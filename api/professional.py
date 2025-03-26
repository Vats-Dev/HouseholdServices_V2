# api/professional.py
from flask import jsonify, request
from . import professional_bp
from models import ServiceRequest, db
from flask_jwt_extended import jwt_required, get_jwt_identity

@professional_bp.route('/accept-request/<int:req_id>', methods=['POST'])
@jwt_required()
def accept_request(req_id):
    professional_id = get_jwt_identity()
    service_request = ServiceRequest.query.get(req_id)
    if service_request and service_request.service_status == 'requested':
        service_request.professional_id = professional_id
        service_request.service_status = 'assigned'
        db.session.commit()
        return jsonify({"message": "Service request accepted!"})
    return jsonify({"error": "Invalid request"}), 400