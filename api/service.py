from flask import jsonify
from . import service_bp
from models import Service

@service_bp.route('/', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{ "id": s.id, "name": s.name, "price": s.price} for s in services])