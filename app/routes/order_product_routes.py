from flask import Blueprint, request, jsonify
from app.models import OrderProduct, Order, Product
from app.schemas import OrderProductSchema
from app import db

order_product_routes = Blueprint('order_product_routes', __name__)

order_product_schema = OrderProductSchema()
order_products_schema = OrderProductSchema(many=True)

@order_product_routes.route('/orderproduct', methods=['POST'])
def add_order_product():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Order_ID') or not data.get('Product_ID') or not data.get('Quantity'):
        return jsonify({'error': 'All fields (Order_ID, Product_ID, Quantity) are required'}), 400

    # Validación de Order_ID, Product_ID y Quantity como enteros positivos
    if not isinstance(data['Order_ID'], int) or data['Order_ID'] <= 0:
        return jsonify({'error': 'Order_ID must be a positive integer'}), 400
    if not isinstance(data['Product_ID'], int) or data['Product_ID'] <= 0:
        return jsonify({'error': 'Product_ID must be a positive integer'}), 400
    if not isinstance(data['Quantity'], int) or data['Quantity'] <= 0:
        return jsonify({'error': 'Quantity must be a positive integer'}), 400

    # Verificar si Order_ID y Product_ID existen
    order = Order.query.get(data['Order_ID'])
    if not order:
        return jsonify({'error': 'Order_ID does not exist in Order table'}), 404
    product = Product.query.get(data['Product_ID'])
    if not product:
        return jsonify({'error': 'Product_ID does not exist in Product table'}), 404

    new_order_product = OrderProduct(
        Order_ID=data['Order_ID'],
        Product_ID=data['Product_ID'],
        Quantity=data['Quantity']
    )
    db.session.add(new_order_product)
    db.session.commit()
    return order_product_schema.jsonify(new_order_product), 201

@order_product_routes.route('/orderproduct', methods=['GET'])
def get_order_products():
    all_order_products = OrderProduct.query.all()
    return order_products_schema.jsonify(all_order_products)

@order_product_routes.route('/orderproduct/<int:order_product_id>', methods=['GET'])
def get_order_product(order_product_id):
    order_product = OrderProduct.query.get_or_404(order_product_id)
    return order_product_schema.jsonify(order_product)

@order_product_routes.route('/orderproduct/<int:order_product_id>', methods=['PUT'])
def update_order_product(order_product_id):
    order_product = OrderProduct.query.get_or_404(order_product_id)
    data = request.get_json()
    order_product.Order_ID = data.get('Order_ID', order_product.Order_ID)
    order_product.Product_ID = data.get('Product_ID', order_product.Product_ID)
    order_product.Quantity = data.get('Quantity', order_product.Quantity)
    db.session.commit()
    return order_product_schema.jsonify(order_product)

@order_product_routes.route('/orderproduct/<int:order_product_id>', methods=['DELETE'])
def delete_order_product(order_product_id):
    order_product = OrderProduct.query.get_or_404(order_product_id)
    db.session.delete(order_product)
    db.session.commit()
    return jsonify({'message': 'OrderProduct deleted successfully'}), 204

# Nueva ruta para ejecutar INNER JOIN entre OrderProduct, Order y Product
@order_product_routes.route('/order_products_with_details', methods=['GET'])
def get_order_products_with_details():
    # Realizar el INNER JOIN entre OrderProduct, Order y Product
    result = db.session.query(OrderProduct, Order, Product).\
        join(Order, OrderProduct.Order_ID == Order.Order_ID).\
        join(Product, OrderProduct.Product_ID == Product.Product_ID).all()
    
    order_products = []
    for order_product, order, product in result:
        order_products.append({
            'Order_Product_ID': order_product.Order_Product_ID,
            'Order_ID': order_product.Order_ID,
            'Product_ID': order_product.Product_ID,
            'Quantity': order_product.Quantity,
            'Order_Date': order.Date,
            'Order_Status': order.Status,
            'Product_Name': product.Product_Name,
            'Product_Price': product.Price
        })
    
    return jsonify(order_products)
