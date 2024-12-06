from flask import Blueprint, request, jsonify
from app.models import Order, Customer, Driver
from app.schemas import OrderSchema
from app import db
from datetime import datetime

order_routes = Blueprint('order_routes', __name__)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_routes.route('/order', methods=['POST'])
def add_order():
    data = request.get_json()

    # Validar formato de fecha (DD/MM/YYYY)
    try:
        parsed_date = datetime.strptime(data['Date'], '%d/%m/%Y')
        data['Date'] = parsed_date.strftime('%Y-%m-%d')  # Convertir a formato ISO para la base de datos
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use DD/MM/YYYY.'}), 400

    # Validación de campos requeridos
    if not data.get('Status') or not data.get('Customer_ID') or not data.get('Driver_ID'):
        return jsonify({'error': 'All fields (Date, Status, Customer_ID, Driver_ID) are required'}), 400

    # Validar claves foráneas
    customer = Customer.query.get(data['Customer_ID'])
    if not customer:
        return jsonify({'error': 'Customer_ID does not exist in Customer table'}), 404
    driver = Driver.query.get(data['Driver_ID'])
    if not driver:
        return jsonify({'error': 'Driver_ID does not exist in Driver table'}), 404

    new_order = Order(
        Date=data['Date'],
        Status=data['Status'],
        Customer_ID=data['Customer_ID'],
        Driver_ID=data['Driver_ID']
    )
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201

@order_routes.route('/order', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    return orders_schema.jsonify(all_orders)

@order_routes.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return order_schema.jsonify(order)

@order_routes.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.Date = data.get('Date', order.Date)
    order.Status = data.get('Status', order.Status)
    order.Customer_ID = data.get('Customer_ID', order.Customer_ID)
    order.Driver_ID = data.get('Driver_ID', order.Driver_ID)
    db.session.commit()
    return order_schema.jsonify(order)

@order_routes.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 204

# Nueva ruta para ejecutar INNER JOIN entre Order, Customer y Driver
@order_routes.route('/orders_with_details', methods=['GET'])
def get_orders_with_details():
    # Realizar el INNER JOIN entre Order, Customer y Driver
    result = db.session.query(Order, Customer, Driver).\
        join(Customer, Order.Customer_ID == Customer.Customer_ID).\
        join(Driver, Order.Driver_ID == Driver.Driver_ID).all()
    
    orders = []
    for order, customer, driver in result:
        orders.append({
            'Order_ID': order.Order_ID,
            'Date': order.Date,
            'Status': order.Status,
            'Customer_Name': customer.Name,
            'Driver_Name': driver.Name
        })
    
    return jsonify(orders)
