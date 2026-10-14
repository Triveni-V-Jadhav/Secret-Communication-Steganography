import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

class EducationalRecommenderSystem:
    """
    Second Syllabus Unit VI: Recommender Systems.
    Implements:
    1. Content-Based Recommendation (TF-IDF cosine similarity of knowledge articles)
    2. Collaborative Filtering (User-Item Matrix User-User / Item-Item Cosine Similarity)
    3. Knowledge-Based Recommendation (Rule-based matching against explicit criteria)
    """
    
    # 1. Content-Based
    @staticmethod
    def content_based_recommend(target_doc_id: str, corpus: Dict[str, str], top_n: int = 3) -> List[Dict]:
        doc_ids = list(corpus.keys())
        if target_doc_id not in doc_ids or len(doc_ids) < 2:
            return []
            
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([corpus[d] for d in doc_ids])
        
        target_idx = doc_ids.index(target_doc_id)
        similarities = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()
        
        # Sort descending excluding self
        ranked_indices = [i for i in np.argsort(similarities)[::-1] if i != target_idx][:top_n]
        
        return [
            {"doc_id": doc_ids[i], "similarity_score": round(float(similarities[i]), 4)}
            for i in ranked_indices
        ]

    # 2. Collaborative Filtering
    @staticmethod
    def collaborative_filtering_demo() -> dict:
        """
        Simulates user rating matrix (5 users x 4 security modules):
        Users rate modules from 1 to 5.
        Uses item-based similarity to recommend unrated modules.
        """
        modules = ["Steganography LSB", "AES-GCM Encryption", "Face Verification", "Anomaly Detection"]
        # Rows: Users (Alice, Bob, Charlie, Dave, Eve), Cols: Modules
        ratings = np.array([
            [5, 5, 2, 0],
            [4, 0, 4, 3],
            [0, 5, 2, 4],
            [3, 4, 0, 5],
            [0, 2, 5, 4]
        ], dtype=np.float32)
        
        # Item similarity
        item_sim = cosine_similarity(ratings.T)
        
        return {
            "modules": modules,
            "user_item_matrix": ratings.tolist(),
            "item_similarity_matrix": np.round(item_sim, 3).tolist(),
            "cold_start_explanation": "New users without ratings encounter the Cold-Start Problem, resolved by Knowledge-Based rules or hybrid defaults."
        }

    # 3. Knowledge-Based
    @staticmethod
    def knowledge_based_recommend(skill_level: str, interest_domain: str) -> List[Dict]:
        """Matches explicit constraints with recommended modules."""
        catalog = [
            {"name": "Steganography Fundamentals", "level": "beginner", "domain": "security", "desc": "Learn LSB bit planes and lossless image embedding."},
            {"name": "Authenticated Cryptography", "level": "intermediate", "domain": "cryptography", "desc": "AES-256-GCM, PBKDF2 key derivation, and integrity tags."},
            {"name": "Biometric Face Verification", "level": "intermediate", "domain": "ai", "desc": "Spatial feature vectors and cosine decision boundaries."},
            {"name": "Deep Sequence Modeling with LSTM", "level": "advanced", "domain": "ai", "desc": "Gating mechanisms, cell states, and vanishing gradient remedies."}
        ]
        
        matched = []
        for item in catalog:
            score = 0
            if item["level"] == skill_level.lower():
                score += 2
            if item["domain"] == interest_domain.lower():
                score += 2
            if score > 0:
                matched.append({**item, "match_score": score})
                
        return sorted(matched, key=lambda x: x["match_score"], reverse=True)
