from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app import app

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passhash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="customer")  # admin, customer, professional
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.passhash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.passhash, password)
    
    service_requests = db.relationship('ServiceRequest', foreign_keys='ServiceRequest.customer_id', backref='customer', cascade="all, delete-orphan")
    assigned_requests = db.relationship('ServiceRequest', foreign_keys='ServiceRequest.professional_id', backref='professional', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id} '{self.username}'>"

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    time_required = db.Column(db.Integer, nullable=False)  # In minutes
    
    requests = db.relationship('ServiceRequest', backref='service', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Service {self.id} '{self.name}'>"

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(20), nullable=False, default="requested")  # requested/assigned/closed
    remarks = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f"<ServiceRequest {self.id} - Service: {self.service_id}, Customer: {self.customer_id}, Status: {self.service_status}>"

with app.app_context():
    db.create_all()
