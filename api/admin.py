# api/admin.py
from flask import jsonify, request
from . import admin_bp
from models import User, Service, db
from flask_jwt_extended import jwt_required

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "role": u.role} for u in users])

@admin_bp.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    data = request.get_json()
    new_service = Service(name=data['name'], price=data['price'], description=data.get('description', ""), time_required=data['time_required'])
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service created successfully!"}), 201