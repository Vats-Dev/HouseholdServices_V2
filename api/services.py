from flask_restful import Resource, reqparse, abort
from models import Service, db
from api import api  # Import the global API instance

# Request parser for creating/updating services
service_parser = reqparse.RequestParser()
service_parser.add_argument('name', type=str, required=True)
service_parser.add_argument('price', type=float, required=True)
service_parser.add_argument('description', type=str)
service_parser.add_argument('time_required', type=int, required=True)

class ServiceList(Resource):
    def get(self):
        services = Service.query.all()
        return [{'id': s.id, 'name': s.name, 'price': s.price, 'description': s.description, 'time_required': s.time_required} for s in services], 200
    
    def post(self):
        args = service_parser.parse_args()
        service = Service(name=args['name'], price=args['price'], description=args['description'], time_required=args['time_required'])
        try:
            db.session.add(service)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error creating service: {str(e)}")
        return {'message': 'Service created successfully', 'service_id': service.id}, 201

class ServiceDetail(Resource):
    def get(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            abort(404, message="Service not found")
        return {'id': service.id, 'name': service.name, 'price': service.price, 'description': service.description, 'time_required': service.time_required}, 200

# Register resources
api.add_resource(ServiceList, '/services')
api.add_resource(ServiceDetail, '/services/<int:service_id>')
