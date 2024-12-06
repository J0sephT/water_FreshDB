# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Inicializar las extensiones
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Cargar configuración
    app.config.from_object('app.config.Config')

    # Inicializar base de datos y marshmallow
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        # Crear todas las tablas en la base de datos
        db.create_all()

        # Registrar rutas (asegúrate de que las rutas estén correctamente definidas)
        from app.routes import (
            driver_routes,
            distribution_route_routes,
            supplier_routes,
            component_routes,
            product_routes,
            customer_routes,
            order_routes,
            order_product_routes,
            driver_route_routes,  # Nueva importación
            product_component_routes  # Nueva importación
        )

        # Registrar blueprints directamente usando el nombre del blueprint
        app.register_blueprint(driver_routes.driver_routes)  
        app.register_blueprint(distribution_route_routes.distribution_route_routes)
        app.register_blueprint(supplier_routes.supplier_routes)
        app.register_blueprint(component_routes.component_routes)
        app.register_blueprint(product_routes.product_routes)
        app.register_blueprint(customer_routes.customer_routes)
        app.register_blueprint(order_routes.order_routes)
        app.register_blueprint(order_product_routes.order_product_routes)
        app.register_blueprint(driver_route_routes.driver_route_routes)  # Nuevo blueprint
        app.register_blueprint(product_component_routes.product_component_routes)  # Nuevo blueprint

    return app
