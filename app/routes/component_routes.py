from flask import Blueprint, request, jsonify
from app.models import Component, Supplier
from app.schemas import ComponentSchema
from app import db

component_routes = Blueprint('component_routes', __name__)

component_schema = ComponentSchema()
components_schema = ComponentSchema(many=True)

@component_routes.route('/component', methods=['POST'])
def add_component():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Component_Name') or not data.get('Description') or not data.get('Supplier_ID'):
        return jsonify({'error': 'All fields (Component_Name, Description, Supplier_ID) are required'}), 400

    # Validación de Supplier_ID como entero positivo
    if not isinstance(data['Supplier_ID'], int) or data['Supplier_ID'] <= 0:
        return jsonify({'error': 'Supplier_ID must be a positive integer'}), 400

    # Verificar si Supplier_ID existe
    supplier = Supplier.query.get(data['Supplier_ID'])
    if not supplier:
        return jsonify({'error': 'Supplier_ID does not exist in Supplier table'}), 404

    # Crear y guardar el nuevo componente
    new_component = Component(
        Component_Name=data['Component_Name'],
        Description=data['Description'],
        Supplier_ID=data['Supplier_ID']
    )
    db.session.add(new_component)
    db.session.commit()
    return component_schema.jsonify(new_component), 201

@component_routes.route('/component', methods=['GET'])
def get_components():
    all_components = Component.query.all()
    return components_schema.jsonify(all_components)

@component_routes.route('/component/<int:component_id>', methods=['GET'])
def get_component(component_id):
    component = Component.query.get_or_404(component_id)
    return component_schema.jsonify(component)

@component_routes.route('/component/<int:component_id>', methods=['PUT'])
def update_component(component_id):
    component = Component.query.get_or_404(component_id)
    data = request.get_json()

    component.Component_Name = data.get('Component_Name', component.Component_Name)
    component.Description = data.get('Description', component.Description)
    component.Supplier_ID = data.get('Supplier_ID', component.Supplier_ID)

    # Validar la existencia del Supplier_ID actualizado
    if component.Supplier_ID:
        supplier = Supplier.query.get(component.Supplier_ID)
        if not supplier:
            return jsonify({'error': 'Supplier_ID does not exist in Supplier table'}), 404

    db.session.commit()
    return component_schema.jsonify(component)

@component_routes.route('/component/<int:component_id>', methods=['DELETE'])
def delete_component(component_id):
    component = Component.query.get_or_404(component_id)
    db.session.delete(component)
    db.session.commit()
    return jsonify({'message': 'Component deleted successfully'}), 204
