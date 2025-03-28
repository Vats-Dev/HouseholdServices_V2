from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models import User, db
from api import api  # Import the global API instance

# Request parser for login
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help="Username is required")
login_parser.add_argument('password', type=str, required=True, help="Password is required")

class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            abort(404, message=f"User {args['username']} does not exist")
        if not user.verify_password(args['password']):
            abort(403, message="Invalid password")

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return {'access_token': access_token}, 200

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        if not user:
            abort(404, message="User not found")
        
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }, 200

# Register resources
api.add_resource(Login, '/user/login')
api.add_resource(UserProfile, '/user/profile')
