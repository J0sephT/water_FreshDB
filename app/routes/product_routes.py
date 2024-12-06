from flask import Blueprint, request, jsonify
from app.models import Product
from app.schemas import ProductSchema
from app import db

product_routes = Blueprint('product_routes', __name__)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@product_routes.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data.get('Product_Name') or not data.get('Description') or not data.get('Price') or not data.get('Stock'):
        return jsonify({'error': 'All fields (Product_Name, Description, Price, Stock) are required'}), 400
    if not isinstance(data['Price'], (int, float)) or data['Price'] <= 0:
        return jsonify({'error': 'Price must be a positive number'}), 400
    if not isinstance(data['Stock'], int) or data['Stock'] < 0:
        return jsonify({'error': 'Stock must be a non-negative integer'}), 400
    new_product = Product(
        Product_Name=data['Product_Name'],
        Description=data['Description'],
        Price=data['Price'],
        Stock=data['Stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@product_routes.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    return products_schema.jsonify(all_products)

@product_routes.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product)

@product_routes.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.Product_Name = data.get('Product_Name', product.Product_Name)
    product.Description = data.get('Description', product.Description)
    product.Price = data.get('Price', product.Price)
    product.Stock = data.get('Stock', product.Stock)
    db.session.commit()
    return product_schema.jsonify(product)

@product_routes.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 204
