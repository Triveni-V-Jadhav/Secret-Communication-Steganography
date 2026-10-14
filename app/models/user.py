import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="USER")  # USER, ADMIN
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    face_profile = db.relationship("FaceProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sent_messages = db.relationship("Message", foreign_keys="Message.sender_id", back_populates="sender", lazy="dynamic", cascade="all, delete-orphan")
    received_messages = db.relationship("Message", foreign_keys="Message.recipient_id", back_populates="recipient", lazy="dynamic")
    audit_logs = db.relationship("AuditLog", back_populates="user", lazy="dynamic")
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password, method="scrypt")
        
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
        
    @property
    def is_admin(self) -> bool:
        return self.role == "ADMIN"
        
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
