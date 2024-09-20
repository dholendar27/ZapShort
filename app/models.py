import uuid
from .extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(100),primary_key = True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    first_name = db.Column(db.String(40),nullable=False)
    last_name = db.Column(db.String(40),nullable=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300),nullable=False)

class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(300), nullable=False)
    shortCode = db.Column(db.String(20), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now)
    updatedAt = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    user_id = db.Column(db.String(100),db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User',backref = db.backref('links',lazy=True))