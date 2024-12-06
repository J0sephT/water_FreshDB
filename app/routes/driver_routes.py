# app/routes/driver_routes.py
from flask import Blueprint, request, jsonify
from app.models import Driver
from app.schemas import DriverSchema
from app import db

# Crear Blueprint
driver_routes = Blueprint('driver_routes', __name__)

driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)

# Rutas
@driver_routes.route('/driver', methods=['POST'])
def add_driver():
    data = request.get_json()
    if not data.get('Name') or not data.get('Phone') or not data.get('Email') or not data.get('ID_Number'):
        return jsonify({'error': 'All fields (Name, Phone, Email, ID_Number) are required'}), 400
    if '@' not in data['Email'] or '.' not in data['Email']:
        return jsonify({'error': 'Invalid email format'}), 400
    new_driver = Driver(
        Name=data['Name'],
        Phone=data['Phone'],
        Email=data['Email'],
        ID_Number=data['ID_Number']
    )
    db.session.add(new_driver)
    db.session.commit()
    return driver_schema.jsonify(new_driver), 201

@driver_routes.route('/driver', methods=['GET'])
def get_drivers():
    all_drivers = Driver.query.all()
    return drivers_schema.jsonify(all_drivers)

@driver_routes.route('/driver/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    return driver_schema.jsonify(driver)

@driver_routes.route('/driver/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    data = request.get_json()
    driver.Name = data.get('Name', driver.Name)
    driver.Phone = data.get('Phone', driver.Phone)
    driver.Email = data.get('Email', driver.Email)
    driver.ID_Number = data.get('ID_Number', driver.ID_Number)
    db.session.commit()
    return driver_schema.jsonify(driver)

@driver_routes.route('/driver/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return jsonify({'message': 'Driver deleted successfully'}), 204
