from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.sql import func

db = SQLAlchemy()


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.String(100), unique=True, nullable=False)
    customer_number = db.Column(db.String(15), nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    chats = db.relationship('Chat', backref='customer',
                            lazy=True, cascade='all, delete-orphan')


class Chat(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    classification = db.Column(db.String(50))
    additional_data = db.Column(JSON, nullable=True)
    current_state = db.Column(db.String(50), nullable=True, default='active')
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    messages = db.relationship(
        'ChatMessage', backref='chat', lazy=True, cascade='all, delete-orphan')


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_uuid = db.Column(db.String(36), db.ForeignKey(
        'chat.uuid'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    is_bot = db.Column(db.Boolean, nullable=False, default=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=func.now())
