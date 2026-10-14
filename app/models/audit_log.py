from datetime import datetime
from app.extensions import db

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    action = db.Column(db.String(64), nullable=False, index=True)
    # e.g., 'AUTH_LOGIN_SUCCESS', 'STEGO_ENCODE', 'STEGO_DECODE_SUCCESS', 'FACE_VERIFY_SUCCESS'
    status = db.Column(db.String(20), nullable=False, default="SUCCESS")  # SUCCESS, FAILURE, DENIED
    ip_address = db.Column(db.String(45), nullable=True)
    details = db.Column(db.String(512), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    user = db.relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog {self.action} status={self.status} at={self.timestamp}>"
