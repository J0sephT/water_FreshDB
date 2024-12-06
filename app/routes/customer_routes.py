# app/routes/customer_routes.py
from flask import Blueprint, request, jsonify
from app.models import Customer
from app.schemas import CustomerSchema
from app import db

# Crear Blueprint
customer_routes = Blueprint('customer_routes', __name__)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Rutas
@customer_routes.route('/customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    if not data.get('Name') or not data.get('Address') or not data.get('Phone') or not data.get('Email'):
        return jsonify({'error': 'All fields (Name, Address, Phone, Email) are required'}), 400
    if '@' not in data['Email'] or '.' not in data['Email']:
        return jsonify({'error': 'Invalid email format'}), 400
    new_customer = Customer(
        Name=data['Name'],
        Address=data['Address'],
        Phone=data['Phone'],
        Email=data['Email']
    )
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customer_routes.route('/customer', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    return customers_schema.jsonify(all_customers)

@customer_routes.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return customer_schema.jsonify(customer)

@customer_routes.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    customer.Name = data.get('Name', customer.Name)
    customer.Address = data.get('Address', customer.Address)
    customer.Phone = data.get('Phone', customer.Phone)
    customer.Email = data.get('Email', customer.Email)
    db.session.commit()
    return customer_schema.jsonify(customer)

@customer_routes.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 204
