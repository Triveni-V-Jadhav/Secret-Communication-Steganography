import pytest
import numpy as np
from app.face_recognition.enrollment import FaceFeatureExtractor
from app.face_recognition.verification import FaceVerificationService
from app.face_recognition.evaluation import BiometricEvaluator

def test_face_feature_cosine_similarity():
    # Identical normalized face simulation (160x160)
    face_a = np.ones((160, 160), dtype=np.uint8) * 128
    feat_a1 = FaceFeatureExtractor.extract_features(face_a)
    feat_a2 = FaceFeatureExtractor.extract_features(face_a)
    
    sim = FaceVerificationService.cosine_similarity(feat_a1, feat_a2)
    assert sim >= 0.999  # Identical images match perfectly

def test_face_feature_disparate_images():
    face_a = np.zeros((160, 160), dtype=np.uint8)
    face_b = np.random.randint(0, 255, (160, 160), dtype=np.uint8)
    
    feat_a = FaceFeatureExtractor.extract_features(face_a)
    feat_b = FaceFeatureExtractor.extract_features(face_b)
    
    sim = FaceVerificationService.cosine_similarity(feat_a, feat_b)
    assert sim < 0.72  # Below verification threshold

def test_biometric_evaluation_eer():
    genuine = [0.85, 0.90, 0.95, 0.88]
    impostor = [0.30, 0.40, 0.50, 0.35]
    
    report = BiometricEvaluator.evaluate_thresholds(genuine, impostor)
    assert "eer" in report
    assert "eval_points" in report
    assert report["eer"] <= 0.25
