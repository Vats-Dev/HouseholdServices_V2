# api/__init__.py
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
customer_bp = Blueprint('customer', __name__, url_prefix='/customer')
professional_bp = Blueprint('professional', __name__, url_prefix='/professional')
service_bp = Blueprint('service', __name__, url_prefix='/service')
service_request_bp = Blueprint('service_request', __name__, url_prefix='/service-request')

# Import views to register routes
from . import admin, auth, customer, professional, service, service_request

def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(professional_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(service_request_bp)