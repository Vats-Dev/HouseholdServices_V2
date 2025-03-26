from flask import jsonify, request
from . import auth_bp
from models import User, db
from flask_jwt_extended import create_access_token

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.verify_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token, "role": user.role})
    return jsonify({"error": "Invalid credentials"}), 401