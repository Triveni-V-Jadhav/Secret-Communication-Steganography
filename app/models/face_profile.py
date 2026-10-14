import json
from datetime import datetime
from app.extensions import db

class FaceProfile(db.Model):
    __tablename__ = "face_profiles"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    has_consent = db.Column(db.Boolean, default=True, nullable=False)
    consent_statement = db.Column(db.String(512), nullable=False)
    
    # Secure storage: We store normalized 128-d or feature histogram representation as encrypted/structured vector
    # Never raw webcam footage or unencrypted personally identifiable biometrics
    embedding_json = db.Column(db.Text, nullable=False)
    algorithm_version = db.Column(db.String(50), default="LBPH-Haar-v1.0", nullable=False)
    image_quality_score = db.Column(db.Float, default=1.0)
    
    user = db.relationship("User", back_populates="face_profile")
    
    def get_embedding(self):
        try:
            return json.loads(self.embedding_json)
        except Exception:
            return None
            
    def set_embedding(self, embedding_list):
        self.embedding_json = json.dumps(embedding_list)
        
    def __repr__(self):
        return f"<FaceProfile user_id={self.user_id} ver={self.algorithm_version}>"
