from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

class TextCategoryClassifier:
    """Classifies educational/security messages into functional intent categories."""
    
    CATEGORIES = ["SECURITY_ALERT", "TECHNICAL_DOCUMENT", "GENERAL_COMMUNICATION", "USER_SUPPORT"]
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=200)
        self.clf = LogisticRegression()
        self._is_trained = False
        self._train_default_baseline()
        
    def _train_default_baseline(self):
        samples = [
            ("Multiple failed login attempts detected on host. Potential brute force.", "SECURITY_ALERT"),
            ("Suspicious unauthorized token extracted from incoming network stream.", "SECURITY_ALERT"),
            ("Steganography chunk embedding completed with zero bit errors.", "TECHNICAL_DOCUMENT"),
            ("AES-256 authenticated encryption specification and RFC requirements.", "TECHNICAL_DOCUMENT"),
            ("Hello teammate, sharing the research report from yesterday's lab.", "GENERAL_COMMUNICATION"),
            ("Meeting scheduled for project evaluation and final code submission.", "GENERAL_COMMUNICATION"),
            ("How do I reset my password if I forget my secret key?", "USER_SUPPORT"),
            ("The image upload failed because file format is JPEG instead of PNG.", "USER_SUPPORT")
        ]
        X = [s[0] for s in samples]
        y = [s[1] for s in samples]
        
        X_vec = self.vectorizer.fit_transform(X)
        self.clf.fit(X_vec, y)
        self._is_trained = True
        
    def predict(self, text: str) -> dict:
        if not text.strip():
            return {"category": "GENERAL_COMMUNICATION", "confidence": 0.5}
            
        X_vec = self.vectorizer.transform([text])
        probs = self.clf.predict_proba(X_vec)[0]
        classes = self.clf.classes_
        
        best_idx = int(np.argmax(probs))
        return {
            "predicted_category": classes[best_idx],
            "confidence": round(float(probs[best_idx]), 4),
            "distribution": {classes[i]: round(float(probs[i]), 3) for i in range(len(classes))}
        }
