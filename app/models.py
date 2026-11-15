from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), default='')
    email = db.Column(db.String(120), default='')

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opening = db.Column(db.Time, nullable=False)
    closing = db.Column(db.Time, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    start = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, default='')
    status = db.Column(db.String(20), nullable=False, default='Agendado')
    client = db.relationship('Client')
    service = db.relationship('Service')
