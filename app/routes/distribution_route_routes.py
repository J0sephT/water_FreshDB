from flask import Blueprint, request, jsonify
from app.models import DistributionRoute
from app.schemas import DistributionRouteSchema
from app import db

distribution_route_routes = Blueprint('distribution_route_routes', __name__)

distribution_route_schema = DistributionRouteSchema()
distribution_routes_schema = DistributionRouteSchema(many=True)

@distribution_route_routes.route('/distributionroute', methods=['POST'])
def add_distribution_route():
    data = request.get_json()
    if not data.get('Description') or not data.get('Frequency'):
        return jsonify({'error': 'All fields (Description, Frequency) are required'}), 400
    if not isinstance(data['Frequency'], int) or data['Frequency'] <= 0:
        return jsonify({'error': 'Frequency must be a positive integer'}), 400
    new_route = DistributionRoute(
        Description=data['Description'],
        Frequency=data['Frequency']
    )
    db.session.add(new_route)
    db.session.commit()
    return distribution_route_schema.jsonify(new_route), 201

@distribution_route_routes.route('/distributionroute', methods=['GET'])
def get_distribution_routes():
    all_routes = DistributionRoute.query.all()
    return distribution_routes_schema.jsonify(all_routes)

@distribution_route_routes.route('/distributionroute/<int:route_id>', methods=['GET'])
def get_distribution_route(route_id):
    route = DistributionRoute.query.get_or_404(route_id)
    return distribution_route_schema.jsonify(route)

@distribution_route_routes.route('/distributionroute/<int:route_id>', methods=['PUT'])
def update_distribution_route(route_id):
    route = DistributionRoute.query.get_or_404(route_id)
    data = request.get_json()
    route.Description = data.get('Description', route.Description)
    route.Frequency = data.get('Frequency', route.Frequency)
    db.session.commit()
    return distribution_route_schema.jsonify(route)

@distribution_route_routes.route('/distributionroute/<int:route_id>', methods=['DELETE'])
def delete_distribution_route(route_id):
    route = DistributionRoute.query.get_or_404(route_id)
    db.session.delete(route)
    db.session.commit()
    return jsonify({'message': 'Distribution Route deleted successfully'}), 204
