from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Service, ServiceRequest
from datetime import datetime

routes = Blueprint("routes", __name__)

# User Registration
@routes.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400
    
    user = User(username=data["username"], email=data["email"], role=data.get("role", "customer"))
    user.password = data["password"]
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# User Login
@routes.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.verify_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "role": user.role})

# Get Current User
@routes.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "role": user.role})

# Create a Service (Admin Only)
@routes.route("/service", methods=["POST"])
@jwt_required()
def create_service():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.json
    service = Service(name=data["name"], price=data["price"], description=data.get("description"), time_required=data["time_required"])
    db.session.add(service)
    db.session.commit()
    return jsonify({"message": "Service created"})

# Get All Services
@routes.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([{ "id": s.id, "name": s.name, "price": s.price, "description": s.description, "time_required": s.time_required } for s in services])

# Request a Service
@routes.route("/request", methods=["POST"])
@jwt_required()
def request_service():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != "customer":
        return jsonify({"error": "Only customers can request services"}), 403
    
    data = request.json
    service = Service.query.get(data["service_id"])
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    request_entry = ServiceRequest(service_id=service.id, customer_id=user.id, service_status="requested")
    db.session.add(request_entry)
    db.session.commit()
    return jsonify({"message": "Service requested successfully"})
