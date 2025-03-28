from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Initialize extensions without an app instance
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

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
    
    services = db.relationship('UserService', back_populates='professional')  # Link to services they offer
    
    def __repr__(self):
        return f"<User {self.id} '{self.username}'>"

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Float, nullable=False)  # Base price
    price = db.Column(db.Float, nullable=False, default=0.0)  # Add price field for consistency
    time_required = db.Column(db.Integer, nullable=False)  # In minutes

    requests = db.relationship('ServiceRequest', backref='service', cascade="all, delete-orphan")
    professionals = db.relationship('UserService', back_populates='service')  # Professionals offering this service

    def __repr__(self):
        return f"<Service {self.id} '{self.name}'>"

class UserService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Custom price by professional
    
    professional = db.relationship('User', back_populates='services')
    service = db.relationship('Service', back_populates='professionals')
    
    def __repr__(self):
        return f"<UserService Professional: {self.professional_id}, Service: {self.service_id}, Price: {self.price}>"

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    scheduled_date = db.Column(db.DateTime, nullable=True)
    date_of_request = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(20), nullable=False, default="requested")  # requested/assigned/closed
    payment_status = db.Column(db.String(20), nullable=False, default="pending")  # pending/paid/refunded
    remarks = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<ServiceRequest {self.id} - Service: {self.service_id}, Customer: {self.customer_id}, Status: {self.service_status}>"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Review {self.id} - Rating: {self.rating}>"

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Notification {self.id} - User: {self.user_id}, Read: {self.is_read}>"