from flask import Blueprint, request, jsonify
from app.models import ProductComponent, Product, Component, Supplier  # Asegúrate de importar Supplier
from app.schemas import ProductComponentSchema
from app import db

# Crear Blueprint para ProductComponent
product_component_routes = Blueprint('product_component_routes', __name__)

# Esquemas
product_component_schema = ProductComponentSchema()
product_components_schema = ProductComponentSchema(many=True)

@product_component_routes.route('/productcomponent', methods=['POST'])
def add_product_component():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Product_ID') or not data.get('Component_ID') or not data.get('Quantity'):
        return jsonify({'error': 'All fields (Product_ID, Component_ID, Quantity) are required'}), 400

    # Validación de Product_ID, Component_ID y Quantity como enteros positivos
    if not isinstance(data['Product_ID'], int) or data['Product_ID'] <= 0:
        return jsonify({'error': 'Product_ID must be a positive integer'}), 400
    if not isinstance(data['Component_ID'], int) or data['Component_ID'] <= 0:
        return jsonify({'error': 'Component_ID must be a positive integer'}), 400
    if not isinstance(data['Quantity'], int) or data['Quantity'] <= 0:
        return jsonify({'error': 'Quantity must be a positive integer'}), 400

    # Verificar si Product_ID y Component_ID existen
    product = Product.query.get(data['Product_ID'])
    if not product:
        return jsonify({'error': 'Product_ID does not exist in Product table'}), 404
    component = Component.query.get(data['Component_ID'])
    if not component:
        return jsonify({'error': 'Component_ID does not exist in Component table'}), 404

    # Crear nuevo ProductComponent
    new_product_component = ProductComponent(
        Product_ID=data['Product_ID'],
        Component_ID=data['Component_ID'],
        Quantity=data['Quantity']
    )
    db.session.add(new_product_component)
    db.session.commit()
    return product_component_schema.jsonify(new_product_component), 201

@product_component_routes.route('/productcomponent', methods=['GET'])
def get_product_components():
    all_product_components = ProductComponent.query.all()
    return product_components_schema.jsonify(all_product_components)

@product_component_routes.route('/productcomponent/<int:product_component_id>', methods=['GET'])
def get_product_component(product_component_id):
    product_component = ProductComponent.query.get_or_404(product_component_id)
    return product_component_schema.jsonify(product_component)

@product_component_routes.route('/productcomponent/<int:product_component_id>', methods=['PUT'])
def update_product_component(product_component_id):
    product_component = ProductComponent.query.get_or_404(product_component_id)
    data = request.get_json()
    product_component.Product_ID = data.get('Product_ID', product_component.Product_ID)
    product_component.Component_ID = data.get('Component_ID', product_component.Component_ID)
    product_component.Quantity = data.get('Quantity', product_component.Quantity)
    db.session.commit()
    return product_component_schema.jsonify(product_component)

@product_component_routes.route('/productcomponent/<int:product_component_id>', methods=['DELETE'])
def delete_product_component(product_component_id):
    product_component = ProductComponent.query.get_or_404(product_component_id)
    db.session.delete(product_component)
    db.session.commit()
    return jsonify({'message': 'ProductComponent deleted successfully'}), 204

# Nueva ruta para INNER JOIN entre Product, Component y ProductComponent
@product_component_routes.route('/productcomponent/join', methods=['GET'])
def get_product_component_join():
    # Realizamos el INNER JOIN entre Product, Component y ProductComponent
    result = db.session.query(Product.Product_Name, Component.Component_Name, ProductComponent.Quantity).\
        join(ProductComponent, Product.Product_ID == ProductComponent.Product_ID).\
        join(Component, ProductComponent.Component_ID == Component.Component_ID).all()

    # Si no hay resultados, devolver mensaje adecuado
    if not result:
        return jsonify({'error': 'No data found'}), 404

    # Transformar los resultados a una lista de diccionarios
    data = []
    for row in result:
        data.append({
            'Product_Name': row[0],
            'Component_Name': row[1],
            'Quantity': row[2]
        })

    return jsonify(data), 200

# Nueva ruta para obtener los componentes de un producto (INNER JOIN con Supplier)
@product_component_routes.route('/product/<int:product_id>/components', methods=['GET'])
def get_components_for_product(product_id):
    result = db.session.query(ProductComponent, Component, Supplier).\
        join(Component, ProductComponent.Component_ID == Component.Component_ID).\
        join(Supplier, Component.Supplier_ID == Supplier.Supplier_ID).\
        filter(ProductComponent.Product_ID == product_id).all()

    # Si no hay resultados, devolver mensaje adecuado
    if not result:
        return jsonify({'error': 'No data found'}), 404

    # Transformar los resultados a una lista de diccionarios
    components = []
    for product_component, component, supplier in result:
        components.append({
            'Product_Component_ID': product_component.Product_Component_ID,
            'Component_Name': component.Component_Name,
            'Description': component.Description,
            'Supplier_Name': supplier.Supplier_Name
        })

    return jsonify(components), 200
