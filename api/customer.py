from flask import jsonify, request
from . import customer_bp
from models import ServiceRequest, db
from flask_jwt_extended import jwt_required, get_jwt_identity

@customer_bp.route('/request-service', methods=['POST'])
@jwt_required()
def request_service():
    data = request.get_json()
    customer_id = get_jwt_identity()
    new_request = ServiceRequest(service_id=data['service_id'], customer_id=customer_id, service_status='requested')
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Service requested successfully!"}), 201