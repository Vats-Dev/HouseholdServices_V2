from flask import jsonify
from . import service_request_bp
from models import ServiceRequest

@service_request_bp.route('/pending', methods=['GET'])
def get_pending_requests():
    requests = ServiceRequest.query.filter_by(service_status='requested').all()
    return jsonify([{ "id": r.id, "service_id": r.service_id, "customer_id": r.customer_id} for r in requests])
