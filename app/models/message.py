from datetime import datetime
from app.extensions import db

class Message(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True)
    message_uuid = db.Column(db.String(36), unique=True, nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    title = db.Column(db.String(128), nullable=False)
    # Metadata only - Confidential message text is NEVER stored plaintext in the DB.
    # It lives strictly inside the stego-package ciphertext or an ephemeral session.
    requires_face_auth = db.Column(db.Boolean, default=False, nullable=False)
    is_delivered = db.Column(db.Boolean, default=False, nullable=False)
    is_extracted = db.Column(db.Boolean, default=False, nullable=False)
    extraction_count = db.Column(db.Integer, default=0, nullable=False)
    
    total_chunks = db.Column(db.Integer, nullable=False, default=1)
    payload_sha256 = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    extracted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = db.relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")
    stego_images = db.relationship("StegoImage", back_populates="message", cascade="all, delete-orphan")
    documents = db.relationship("Document", back_populates="message", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Message uuid={self.message_uuid} chunks={self.total_chunks}>"
