from flask import Blueprint, request, jsonify
from app.models import DriverRoute, Driver, DistributionRoute
from app.schemas import DriverRouteSchema
from app import db

driver_route_routes = Blueprint('driver_route_routes', __name__)

driver_route_schema = DriverRouteSchema()
driver_routes_schema = DriverRouteSchema(many=True)

# Ruta para agregar una nueva asignación de ruta a un conductor
@driver_route_routes.route('/driverroute', methods=['POST'])
def add_driver_route():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('Driver_ID') or not data.get('Route_ID'):
        return jsonify({'error': 'Both Driver_ID and Route_ID are required'}), 400

    # Validar si el Driver_ID existe
    driver = Driver.query.get(data['Driver_ID'])
    if not driver:
        return jsonify({'error': 'Driver_ID does not exist in Driver table'}), 404

    # Validar si el Route_ID existe
    route = DistributionRoute.query.get(data['Route_ID'])
    if not route:
        return jsonify({'error': 'Route_ID does not exist in DistributionRoute table'}), 404

    new_driver_route = DriverRoute(
        Driver_ID=data['Driver_ID'],
        Route_ID=data['Route_ID']
    )
    db.session.add(new_driver_route)
    db.session.commit()
    return driver_route_schema.jsonify(new_driver_route), 201

# Ruta para obtener todas las asignaciones de rutas
@driver_route_routes.route('/driverroute', methods=['GET'])
def get_driver_routes():
    all_driver_routes = DriverRoute.query.all()
    return driver_routes_schema.jsonify(all_driver_routes)

# Ruta para obtener una asignación de ruta por su ID
@driver_route_routes.route('/driverroute/<int:driver_route_id>', methods=['GET'])
def get_driver_route(driver_route_id):
    driver_route = DriverRoute.query.get_or_404(driver_route_id)
    return driver_route_schema.jsonify(driver_route)

# Ruta para actualizar una asignación de ruta por su ID
@driver_route_routes.route('/driverroute/<int:driver_route_id>', methods=['PUT'])
def update_driver_route(driver_route_id):
    driver_route = DriverRoute.query.get_or_404(driver_route_id)
    data = request.get_json()

    driver_route.Driver_ID = data.get('Driver_ID', driver_route.Driver_ID)
    driver_route.Route_ID = data.get('Route_ID', driver_route.Route_ID)

    # Validar si el Driver_ID y Route_ID existen
    if driver_route.Driver_ID:
        driver = Driver.query.get(driver_route.Driver_ID)
        if not driver:
            return jsonify({'error': 'Driver_ID does not exist in Driver table'}), 404

    if driver_route.Route_ID:
        route = DistributionRoute.query.get(driver_route.Route_ID)
        if not route:
            return jsonify({'error': 'Route_ID does not exist in DistributionRoute table'}), 404

    db.session.commit()
    return driver_route_schema.jsonify(driver_route)

# Ruta para eliminar una asignación de ruta por su ID
@driver_route_routes.route('/driverroute/<int:driver_route_id>', methods=['DELETE'])
def delete_driver_route(driver_route_id):
    driver_route = DriverRoute.query.get_or_404(driver_route_id)
    db.session.delete(driver_route)
    db.session.commit()
    return jsonify({'message': 'DriverRoute deleted successfully'}), 204
