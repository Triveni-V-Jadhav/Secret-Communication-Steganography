import numpy as np
import cv2
from app.face_recognition.preprocessing import FacePreprocessor

class FaceFeatureExtractor:
    """
    Extracts spatial-frequency feature vectors and Local Binary Patterns (LBPH)
    compatible with lightweight local CPU inference without requiring multi-gigabyte models.
    """
    
    @staticmethod
    def extract_features(normalized_face_gray: np.ndarray) -> list:
        """
        Computes a normalized 128-dimensional spatial grid histogram representation.
        Divides the 160x160 face into 4x4 sub-regions (16 cells) and calculates 8-bin gradient/intensity
        features for each cell -> 16 * 8 = 128-dimensional embedding.
        """
        h, w = normalized_face_gray.shape
        cell_h, cell_w = h // 4, w // 4
        features = []
        
        for r in range(4):
            for c in range(4):
                cell = normalized_face_gray[r*cell_h:(r+1)*cell_h, c*cell_w:(c+1)*cell_w]
                # Compute gradient magnitude
                gx = cv2.Sobel(cell, cv2.CV_32F, 1, 0, ksize=3)
                gy = cv2.Sobel(cell, cv2.CV_32F, 0, 1, ksize=3)
                mag = cv2.magnitude(gx, gy)
                
                # 8-bin histogram of cell
                hist, _ = np.histogram(mag, bins=8, range=(0, 256))
                features.extend(hist.tolist())
                
        feat_arr = np.array(features, dtype=np.float32)
        norm = np.linalg.norm(feat_arr)
        if norm > 0:
            feat_arr = feat_arr / norm
            
        return feat_arr.tolist()

class FaceEnrollmentService:
    """
    Privacy-conscious enrollment service. Requires explicit user consent statement
    and stores only non-reversible normalized feature vectors.
    """
    
    @staticmethod
    def enroll_face(image_bytes: bytes, consent_statement: str) -> dict:
        if not consent_statement or "consent" not in consent_statement.lower():
            return {
                "success": False,
                "error": "Explicit consent is required. You must check the consent statement to enroll your biometric template."
            }
            
        face_img, status, msg = FacePreprocessor.detect_and_align_face(image_bytes)
        if status != "SUCCESS":
            return {"success": False, "error": msg, "code": status}
            
        embedding = FaceFeatureExtractor.extract_features(face_img)
        
        return {
            "success": True,
            "embedding": embedding,
            "algorithm": "SpatialGradient-128D-v1.0",
            "message": "Face profile successfully extracted and ready for secure template storage."
        }
