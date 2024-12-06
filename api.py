from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError, validate
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ojalasalga200.@localhost:3307/WaterFresh_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Modelos de la Base de Datos
class Driver(db.Model):
    __tablename__ = 'driver'
    Driver_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    ID_Number = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Order', backref='driver', lazy=True, cascade="all, delete-orphan")

class DistributionRoute(db.Model):
    __tablename__ = 'distribution_route'
    Route_ID = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(255), nullable=False)
    Frequency = db.Column(db.Integer, nullable=False)
    driver_routes = db.relationship('DriverRoute', backref='route', lazy=True, cascade="all, delete-orphan")

class DriverRoute(db.Model):
    __tablename__ = 'driver_route'
    Driver_Route_ID = db.Column(db.Integer, primary_key=True)
    Driver_ID = db.Column(db.Integer, db.ForeignKey('driver.Driver_ID'), nullable=False)
    Route_ID = db.Column(db.Integer, db.ForeignKey('distribution_route.Route_ID'), nullable=False)

class Supplier(db.Model):
    __tablename__ = 'supplier'
    Supplier_ID = db.Column(db.Integer, primary_key=True)
    Supplier_Name = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    components = db.relationship('Component', backref='supplier', lazy=True, cascade="all, delete-orphan")

class Component(db.Model):
    __tablename__ = 'component'
    Component_ID = db.Column(db.Integer, primary_key=True)
    Component_Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Supplier_ID = db.Column(db.Integer, db.ForeignKey('supplier.Supplier_ID'), nullable=False)
    product_components = db.relationship('ProductComponent', backref='component', lazy=True, cascade="all, delete-orphan")

class Product(db.Model):
    __tablename__ = 'product'
    Product_ID = db.Column(db.Integer, primary_key=True)
    Product_Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Stock = db.Column(db.Integer, nullable=False)
    product_components = db.relationship('ProductComponent', backref='product', lazy=True, cascade="all, delete-orphan")
    order_products = db.relationship('OrderProduct', backref='product', lazy=True, cascade="all, delete-orphan")

class ProductComponent(db.Model):
    __tablename__ = 'product_component'
    Product_Component_ID = db.Column(db.Integer, primary_key=True)
    Product_ID = db.Column(db.Integer, db.ForeignKey('product.Product_ID'), nullable=False)
    Component_ID = db.Column(db.Integer, db.ForeignKey('component.Component_ID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)

class Customer(db.Model):
    __tablename__ = 'customer'
    Customer_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Address = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True, cascade="all, delete-orphan")

class Order(db.Model):
    __tablename__ = 'order'
    Order_ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(20), nullable=False)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('customer.Customer_ID'), nullable=False)
    Driver_ID = db.Column(db.Integer, db.ForeignKey('driver.Driver_ID'), nullable=False)
    order_products = db.relationship('OrderProduct', backref='order', lazy=True, cascade="all, delete-orphan")

class OrderProduct(db.Model):
    __tablename__ = 'order_product'
    Order_Product_ID = db.Column(db.Integer, primary_key=True)
    Order_ID = db.Column(db.Integer, db.ForeignKey('order.Order_ID'), nullable=False)
    Product_ID = db.Column(db.Integer, db.ForeignKey('product.Product_ID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)



# Esquemas para Serialización y Validación
class DriverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Driver
        load_instance = True

class DistributionRouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DistributionRoute
        load_instance = True

class DriverRouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DriverRoute
        load_instance = True

class SupplierSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Supplier
        load_instance = True

class ComponentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Component
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class ProductComponentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductComponent
        load_instance = True

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True

class OrderProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderProduct
        load_instance = True

# Crear la base de datos
with app.app_context():
    db.create_all()

# Esquemas para serialización
driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)
distribution_route_schema = DistributionRouteSchema()
distribution_routes_schema = DistributionRouteSchema(many=True)
driver_route_schema = DriverRouteSchema()
driver_routes_schema = DriverRouteSchema(many=True)
supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many=True)
component_schema = ComponentSchema()
components_schema = ComponentSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
product_component_schema = ProductComponentSchema()
product_components_schema = ProductComponentSchema(many=True)
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_product_schema = OrderProductSchema()
order_products_schema = OrderProductSchema(many=True)

# ----------------------- Endpoints CRUD -----------------------
# Patrón para todas las tablas: POST, GET, PUT, DELETE.

# CRUD para Driver
@app.route('/driver', methods=['POST'])
def add_driver():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Name') or not data.get('Phone') or not data.get('Email') or not data.get('ID_Number'):
        return jsonify({'error': 'All fields (Name, Phone, Email, ID_Number) are required'}), 400

    # Validación del formato de Email
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


@app.route('/driver', methods=['GET'])
def get_drivers():
    all_drivers = Driver.query.all()
    return driver_schema.jsonify(all_drivers, many=True)

@app.route('/driver/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    return driver_schema.jsonify(driver)

@app.route('/driver/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    data = request.get_json()
    driver.Name = data.get('Name', driver.Name)
    driver.Phone = data.get('Phone', driver.Phone)
    driver.Email = data.get('Email', driver.Email)
    driver.ID_Number = data.get('ID_Number', driver.ID_Number)
    db.session.commit()
    return driver_schema.jsonify(driver)

@app.route('/driver/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return jsonify({'message': 'Driver deleted successfully'}), 204

# CRUD para DistributionRoute
@app.route('/distributionroute', methods=['POST'])
def add_distribution_route():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Description') or not data.get('Frequency'):
        return jsonify({'error': 'All fields (Description, Frequency) are required'}), 400

    # Validación de Frequency como entero positivo
    if not isinstance(data['Frequency'], int) or data['Frequency'] <= 0:
        return jsonify({'error': 'Frequency must be a positive integer'}), 400

    new_route = DistributionRoute(
        Description=data['Description'],
        Frequency=data['Frequency']
    )
    db.session.add(new_route)
    db.session.commit()
    return distribution_route_schema.jsonify(new_route), 201


@app.route('/distributionroute', methods=['GET'])
def get_distribution_routes():
    all_routes = DistributionRoute.query.all()
    return distribution_route_schema.jsonify(all_routes, many=True)

@app.route('/distributionroute/<int:route_id>', methods=['GET'])
def get_distribution_route(route_id):
    route = DistributionRoute.query.get_or_404(route_id)
    return distribution_route_schema.jsonify(route)

@app.route('/distributionroute/<int:route_id>', methods=['PUT'])
def update_distribution_route(route_id):
    route = DistributionRoute.query.get_or_404(route_id)
    data = request.get_json()
    route.Description = data.get('Description', route.Description)
    route.Frequency = data.get('Frequency', route.Frequency)
    db.session.commit()
    return distribution_route_schema.jsonify(route)

@app.route('/distributionroute/<int:route_id>', methods=['DELETE'])
def delete_distribution_route(route_id):
    route = DistributionRoute.query.get_or_404(route_id)
    db.session.delete(route)
    db.session.commit()
    return jsonify({'message': 'Distribution Route deleted successfully'}), 204

#supplier
@app.route('/supplier', methods=['POST'])
def add_supplier():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Supplier_Name') or not data.get('Phone'):
        return jsonify({'error': 'All fields (Supplier_Name, Phone) are required'}), 400

    new_supplier = Supplier(
        Supplier_Name=data['Supplier_Name'],
        Phone=data['Phone']
    )
    db.session.add(new_supplier)
    db.session.commit()
    return supplier_schema.jsonify(new_supplier), 201


@app.route('/supplier', methods=['GET'])
def get_suppliers():
    all_suppliers = Supplier.query.all()
    return supplier_schema.jsonify(all_suppliers, many=True)

@app.route('/supplier/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return supplier_schema.jsonify(supplier)

@app.route('/supplier/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()
    supplier.Supplier_Name = data.get('Supplier_Name', supplier.Supplier_Name)
    supplier.Phone = data.get('Phone', supplier.Phone)
    db.session.commit()
    return supplier_schema.jsonify(supplier)

@app.route('/supplier/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted successfully'}), 204

#component
@app.route('/component', methods=['POST'])
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

    new_component = Component(
        Component_Name=data['Component_Name'],
        Description=data['Description'],
        Supplier_ID=data['Supplier_ID']
    )
    db.session.add(new_component)
    db.session.commit()
    return component_schema.jsonify(new_component), 201


@app.route('/component', methods=['GET'])
def get_components():
    all_components = Component.query.all()
    return component_schema.jsonify(all_components, many=True)

@app.route('/component/<int:component_id>', methods=['GET'])
def get_component(component_id):
    component = Component.query.get_or_404(component_id)
    return component_schema.jsonify(component)

@app.route('/component/<int:component_id>', methods=['PUT'])
def update_component(component_id):
    component = Component.query.get_or_404(component_id)
    data = request.get_json()
    component.Component_Name = data.get('Component_Name', component.Component_Name)
    component.Description = data.get('Description', component.Description)
    component.Supplier_ID = data.get('Supplier_ID', component.Supplier_ID)
    db.session.commit()
    return component_schema.jsonify(component)

@app.route('/component/<int:component_id>', methods=['DELETE'])
def delete_component(component_id):
    component = Component.query.get_or_404(component_id)
    db.session.delete(component)
    db.session.commit()
    return jsonify({'message': 'Component deleted successfully'}), 204

#product
@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Product_Name') or not data.get('Description') or not data.get('Price') or not data.get('Stock'):
        return jsonify({'error': 'All fields (Product_Name, Description, Price, Stock) are required'}), 400

    # Validación de Price y Stock como valores positivos
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


@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    return product_schema.jsonify(all_products, many=True)

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product)

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.Product_Name = data.get('Product_Name', product.Product_Name)
    product.Description = data.get('Description', product.Description)
    product.Price = data.get('Price', product.Price)
    product.Stock = data.get('Stock', product.Stock)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 204

#custumer
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Name') or not data.get('Address') or not data.get('Phone') or not data.get('Email'):
        return jsonify({'error': 'All fields (Name, Address, Phone, Email) are required'}), 400

    # Validación del formato de Email
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


@app.route('/customer', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    return customers_schema.jsonify(all_customers, many=True)

@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return customer_schema.jsonify(customer)

@app.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    customer.Name = data.get('Name', customer.Name)
    customer.Address = data.get('Address', customer.Address)
    customer.Phone = data.get('Phone', customer.Phone)
    customer.Email = data.get('Email', customer.Email)
    db.session.commit()
    return customer_schema.jsonify(customer)

@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 204

#order
from datetime import datetime

@app.route('/order', methods=['POST'])
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

    # Crear y guardar la nueva orden
    new_order = Order(
        Date=data['Date'],
        Status=data['Status'],
        Customer_ID=data['Customer_ID'],
        Driver_ID=data['Driver_ID']
    )
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201



@app.route('/order', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    return orders_schema.jsonify(all_orders, many=True)

@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return order_schema.jsonify(order)

@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.Date = data.get('Date', order.Date)
    order.Status = data.get('Status', order.Status)
    order.Customer_ID = data.get('Customer_ID', order.Customer_ID)
    order.Driver_ID = data.get('Driver_ID', order.Driver_ID)
    db.session.commit()
    return order_schema.jsonify(order)

@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 204

@app.route('/productcomponent', methods=['POST'])
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

    # Verificar si Product_ID existe
    product = Product.query.get(data['Product_ID'])
    if not product:
        return jsonify({'error': 'Product_ID does not exist in Product table'}), 404

    # Verificar si Component_ID existe
    component = Component.query.get(data['Component_ID'])
    if not component:
        return jsonify({'error': 'Component_ID does not exist in Component table'}), 404

    # Crear y guardar el nuevo ProductComponent
    new_product_component = ProductComponent(
        Product_ID=data['Product_ID'],
        Component_ID=data['Component_ID'],
        Quantity=data['Quantity']
    )
    db.session.add(new_product_component)
    db.session.commit()
    return product_component_schema.jsonify(new_product_component), 201


@app.route('/productcomponent', methods=['GET'])
def get_product_components():
    all_product_components = ProductComponent.query.all()
    return product_components_schema.jsonify(all_product_components, many=True)

@app.route('/productcomponent/<int:product_component_id>', methods=['GET'])
def get_product_component(product_component_id):
    product_component = ProductComponent.query.get_or_404(product_component_id)
    return product_component_schema.jsonify(product_component)

@app.route('/productcomponent/<int:product_component_id>', methods=['PUT'])
def update_product_component(product_component_id):
    product_component = ProductComponent.query.get_or_404(product_component_id)
    data = request.get_json()
    product_component.Product_ID = data.get('Product_ID', product_component.Product_ID)
    product_component.Component_ID = data.get('Component_ID', product_component.Component_ID)
    product_component.Quantity = data.get('Quantity', product_component.Quantity)
    db.session.commit()
    return product_component_schema.jsonify(product_component)

@app.route('/productcomponent/<int:product_component_id>', methods=['DELETE'])
def delete_product_component(product_component_id):
    product_component = ProductComponent.query.get_or_404(product_component_id)
    db.session.delete(product_component)
    db.session.commit()
    return jsonify({'message': 'ProductComponent deleted successfully'}), 204

#order product
@app.route('/orderproduct', methods=['POST'])
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


@app.route('/orderproduct', methods=['GET'])
def get_order_products():
    all_order_products = OrderProduct.query.all()
    return order_products_schema.jsonify(all_order_products, many=True)

@app.route('/orderproduct/<int:order_product_id>', methods=['GET'])
def get_order_product(order_product_id):
    order_product = OrderProduct.query.get_or_404(order_product_id)
    return order_product_schema.jsonify(order_product)

@app.route('/orderproduct/<int:order_product_id>', methods=['PUT'])
def update_order_product(order_product_id):
    order_product = OrderProduct.query.get_or_404(order_product_id)
    data = request.get_json()
    order_product.Order_ID = data.get('Order_ID', order_product.Order_ID)
    order_product.Product_ID = data.get('Product_ID', order_product.Product_ID)
    order_product.Quantity = data.get('Quantity', order_product.Quantity)
    db.session.commit()
    return order_product_schema.jsonify(order_product)

@app.route('/orderproduct/<int:order_product_id>', methods=['DELETE'])
def delete_order_product(order_product_id):
    order_product = OrderProduct.query.get_or_404(order_product_id)
    db.session.delete(order_product)
    db.session.commit()
    return jsonify({'message': 'OrderProduct deleted successfully'}), 204

if __name__ == "__main__":
    app.run(debug=True)
