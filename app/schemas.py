# app/schemas.py
from app import ma
from marshmallow import fields, validate
from app.models import (
    Driver,
    DistributionRoute,
    DriverRoute,
    Supplier,
    Component,
    Product,
    ProductComponent,
    Customer,
    Order,
    OrderProduct,
)

class DriverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Driver
        load_instance = True

    orders = fields.List(fields.Nested('OrderSchema', only=["Order_ID", "Status"]))  # Relación con OrderSchema

class DistributionRouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DistributionRoute
        load_instance = True

class DriverRouteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DriverRoute
        load_instance = True

    driver = fields.Nested('DriverSchema', only=['Driver_ID', 'Name'])  # Relación con DriverSchema
    route = fields.Nested('DistributionRouteSchema', only=['Route_ID', 'Description'])  # Relación con DistributionRouteSchema

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

    product_components = fields.List(fields.Nested('ProductComponentSchema', only=["Product_Component_ID", "Quantity"]))  # Relación con ProductComponentSchema

class ProductComponentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductComponent
        load_instance = True

    product = fields.Nested('ProductSchema', only=["Product_ID", "Product_Name"])  # Relación con ProductSchema
    component = fields.Nested('ComponentSchema', only=["Component_ID", "Component_Name"])  # Relación con ComponentSchema

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True

    Email = fields.String(validate=validate.Email())  # Corregido aquí con la validación correcta

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True

    order_products = fields.List(fields.Nested('OrderProductSchema'))  # Relación con OrderProductSchema

class OrderProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderProduct
        load_instance = True
