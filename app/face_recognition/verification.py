import numpy as np
from app.face_recognition.preprocessing import FacePreprocessor
from app.face_recognition.enrollment import FaceFeatureExtractor

class FaceVerificationService:
    """
    Compares live probe image against enrolled biometric feature template
    using Cosine Similarity with configurable decision threshold.
    """
    
    DEFAULT_THRESHOLD = 0.65  # Balanced decision boundary (handles real-world webcam variance)
    
    @staticmethod
    def cosine_similarity(v1: list, v2: list) -> float:
        a = np.array(v1, dtype=np.float32)
        b = np.array(v2, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    @classmethod
    def verify_probe(cls, probe_image_bytes: bytes, enrolled_embedding: list, threshold: float = None) -> dict:
        """
        Verifies a live probe image against an enrolled embedding.
        Returns match decision, confidence score, and metrics.
        """
        if threshold is None:
            threshold = cls.DEFAULT_THRESHOLD
            
        if not enrolled_embedding:
            return {
                "verified": False,
                "error": "No enrolled face profile found for this recipient.",
                "code": "NO_TEMPLATE"
            }
            
        face_img, status, msg = FacePreprocessor.detect_and_align_face(probe_image_bytes)
        if status != "SUCCESS":
            return {
                "verified": False,
                "error": msg,
                "code": status
            }
            
        probe_embedding = FaceFeatureExtractor.extract_features(face_img)
        similarity = cls.cosine_similarity(probe_embedding, enrolled_embedding)
        
        # Distance metric (Cosine distance = 1 - similarity)
        cosine_distance = 1.0 - similarity
        is_match = similarity >= threshold
        
        return {
            "verified": is_match,
            "similarity_score": round(similarity, 4),
            "distance": round(cosine_distance, 4),
            "threshold": threshold,
            "status": "MATCH" if is_match else "NON_MATCH",
            "message": "Identity verified successfully." if is_match else "Biometric verification failed. Face probe does not match recipient profile.",
            "disclaimer": "Notice: Biometric facial verification is probabilistic and provides secondary identity assurance, not sole authentication."
        }
