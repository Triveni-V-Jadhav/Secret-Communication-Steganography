from datetime import datetime
from app.extensions import db

class StegoImage(db.Model):
    __tablename__ = "stego_images"
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    chunk_index = db.Column(db.Integer, nullable=False)  # 0-indexed (e.g., chunk 0 of 3)
    total_chunks = db.Column(db.Integer, nullable=False)
    
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    
    image_width = db.Column(db.Integer, nullable=False)
    image_height = db.Column(db.Integer, nullable=False)
    bytes_capacity = db.Column(db.Integer, nullable=False)
    bytes_embedded = db.Column(db.Integer, nullable=False)
    chunk_sha256 = db.Column(db.String(64), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    message = db.relationship("Message", back_populates="stego_images")
    
    def __repr__(self):
        return f"<StegoImage chunk={self.chunk_index}/{self.total_chunks} file={self.filename}>"
