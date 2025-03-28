from flask_restful import Api
from flask import Blueprint

# Define a blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# Import all resources to register them
from api import auth, users, services, service_requests
