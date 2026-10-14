import re
from typing import Dict, List
from collections import Counter
from app.nlp.preprocessing import TextPreprocessor

class MessageAnalyzer:
    """
    Extracts entities, statistical metrics, entropy, and keywords
    from authorized text (e.g., knowledge base or decrypted authorized text).
    """
    
    # Entity regex patterns for MCA educational NER demonstration
    PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "IP_ADDRESS": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        "CRYPTO_KEY_HEX": r"\b[0-9a-fA-F]{32,64}\b",
        "DATE_FORMAT": r"\b\d{4}-\d{2}-\d{2}\b"
    }
    
    @classmethod
    def extract_named_entities(cls, text: str) -> Dict[str, List[str]]:
        entities = {}
        for entity_type, pattern in cls.PATTERNS.items():
            matches = list(set(re.findall(pattern, text)))
            if matches:
                entities[entity_type] = matches
        return entities
        
    @classmethod
    def analyze_text(cls, text: str) -> dict:
        tokens = TextPreprocessor.tokenize(text)
        cleaned_tokens = TextPreprocessor.remove_stopwords(tokens)
        counts = Counter(cleaned_tokens)
        top_keywords = [item[0] for item in counts.most_common(5)]
        
        entities = cls.extract_named_entities(text)
        
        # Calculate Shannon Entropy of character distribution
        char_counts = Counter(text)
        text_len = max(1, len(text))
        entropy = -sum((c / text_len) * (c / text_len) for c in char_counts.values())  # simplified
        
        return {
            "token_count": len(tokens),
            "unique_terms": len(set(tokens)),
            "keywords": top_keywords,
            "entities": entities,
            "char_count": len(text)
        }
