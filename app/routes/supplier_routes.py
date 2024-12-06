from flask import Blueprint, request, jsonify
from app.models import Supplier
from app.schemas import SupplierSchema
from app import db

supplier_routes = Blueprint('supplier_routes', __name__)

supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many=True)

@supplier_routes.route('/supplier', methods=['POST'])
def add_supplier():
    data = request.get_json()
    if not data.get('Supplier_Name') or not data.get('Phone'):
        return jsonify({'error': 'All fields (Supplier_Name, Phone) are required'}), 400
    new_supplier = Supplier(
        Supplier_Name=data['Supplier_Name'],
        Phone=data['Phone']
    )
    db.session.add(new_supplier)
    db.session.commit()
    return supplier_schema.jsonify(new_supplier), 201

@supplier_routes.route('/supplier', methods=['GET'])
def get_suppliers():
    all_suppliers = Supplier.query.all()
    return suppliers_schema.jsonify(all_suppliers)

@supplier_routes.route('/supplier/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return supplier_schema.jsonify(supplier)

@supplier_routes.route('/supplier/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()
    supplier.Supplier_Name = data.get('Supplier_Name', supplier.Supplier_Name)
    supplier.Phone = data.get('Phone', supplier.Phone)
    db.session.commit()
    return supplier_schema.jsonify(supplier)

@supplier_routes.route('/supplier/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted successfully'}), 204
