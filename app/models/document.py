from datetime import datetime
from app.extensions import db

class Document(db.Model):
    __tablename__ = "documents"
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id", ondelete="CASCADE"), nullable=True)
    
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size_bytes = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False, default="application/octet-stream")
    file_sha256 = db.Column(db.String(64), nullable=False)
    
    is_knowledge_base = db.Column(db.Boolean, default=False, nullable=False)
    title = db.Column(db.String(255), nullable=True)
    content_text = db.Column(db.Text, nullable=True)  # Plain text indexable for KB docs only
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    message = db.relationship("Message", back_populates="documents")
    
    def __repr__(self):
        return f"<Document {self.filename} kb={self.is_knowledge_base}>"
