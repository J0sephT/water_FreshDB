# app/models.py
from app import db

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
    driver_routes = db.relationship('DriverRoute', backref='route', lazy=True)

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
    components = db.relationship('Component', backref='supplier', lazy=True)

class Component(db.Model):
    __tablename__ = 'component'
    Component_ID = db.Column(db.Integer, primary_key=True)
    Component_Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Supplier_ID = db.Column(db.Integer, db.ForeignKey('supplier.Supplier_ID'), nullable=False)
    product_components = db.relationship('ProductComponent', backref='component', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    Product_ID = db.Column(db.Integer, primary_key=True)
    Product_Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Stock = db.Column(db.Integer, nullable=False)
    product_components = db.relationship('ProductComponent', backref='product', lazy=True)
    order_products = db.relationship('OrderProduct', backref='product', lazy=True)

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
    orders = db.relationship('Order', backref='customer', lazy=True)

class Order(db.Model):
    __tablename__ = 'order'
    Order_ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(20), nullable=False)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('customer.Customer_ID'), nullable=False)
    Driver_ID = db.Column(db.Integer, db.ForeignKey('driver.Driver_ID'), nullable=False)
    order_products = db.relationship('OrderProduct', backref='order', lazy=True)

class OrderProduct(db.Model):
    __tablename__ = 'order_product'
    Order_Product_ID = db.Column(db.Integer, primary_key=True)
    Order_ID = db.Column(db.Integer, db.ForeignKey('order.Order_ID'), nullable=False)
    Product_ID = db.Column(db.Integer, db.ForeignKey('product.Product_ID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
