from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ServiceRequest, db, User
from api import api  # Import the global API instance

request_parser = reqparse.RequestParser()
request_parser.add_argument('service_id', type=int, required=True)
request_parser.add_argument('remarks', type=str)

class ServiceRequestList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")

        requests = ServiceRequest.query.filter_by(customer_id=user.id).all()
        return [{'id': r.id, 'service_id': r.service_id, 'status': r.service_status, 'remarks': r.remarks} for r in requests], 200

    @jwt_required()
    def post(self):
        args = request_parser.parse_args()
        user_id = get_jwt_identity()
        
        request = ServiceRequest(service_id=args['service_id'], customer_id=user_id, service_status="requested", remarks=args.get('remarks'))
        try:
            db.session.add(request)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error creating service request: {str(e)}")
        return {'message': 'Service request created successfully', 'request_id': request.id}, 201

api.add_resource(ServiceRequestList, '/service_requests')
