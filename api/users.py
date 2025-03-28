from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from api import api

# Request parser for user registration
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help="Username is required")
user_parser.add_argument('email', type=str, required=True, help="Email is required")
user_parser.add_argument('password', type=str, required=True, help="Password is required")
user_parser.add_argument('role', type=str, choices=('customer', 'professional', 'admin'), default='customer')

# Fields for marshalling the output
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'role': fields.String,
    'created_at': fields.DateTime
}

class UserResource(Resource):
    """Handles user profile retrieval"""
    @marshal_with(user_fields)
    @jwt_required()
    def get(self):
        """Get the current user's profile"""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return user, 200

class UserRegister(Resource):
    """Handles user registration"""
    def post(self):
        """Register a new user"""
        args = user_parser.parse_args()
        
        # Check if username or email already exists
        if User.query.filter_by(username=args['username']).first():
            abort(400, message="Username already taken")
        if User.query.filter_by(email=args['email']).first():
            abort(400, message="Email already registered")
        
        # Create new user
        new_user = User(username=args['username'], email=args['email'])
        new_user.password = args['password']  # TODO: Hash this before saving!
        new_user.role = args['role']
        
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"Error creating user: {str(e)}")
        
        return {'message': 'User registered successfully', 'user_id': new_user.id}, 201

# Add resources to the API
api.add_resource(UserResource, '/users/me')  # User profile
api.add_resource(UserRegister, '/user/register')  # Registration
