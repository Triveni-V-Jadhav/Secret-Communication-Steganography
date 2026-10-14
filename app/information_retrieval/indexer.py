from collections import defaultdict
from typing import List, Dict, Set
from app.nlp.preprocessing import TextPreprocessor

class InvertedIndex:
    """
    Inverted Index structure:
    term -> list of (doc_id, term_frequency, positions)
    """
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(list))
        self.doc_lengths = {}
        self.doc_metadata = {}
        self.total_docs = 0
        
    def add_document(self, doc_id: str, text: str, metadata: dict = None):
        tokens = TextPreprocessor.tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)
        self.doc_metadata[doc_id] = metadata or {}
        self.total_docs += 1
        
        for pos, term in enumerate(tokens):
            self.index[term][doc_id].append(pos)
            
    def get_postings(self, term: str) -> Dict[str, int]:
        """Returns dict of doc_id -> frequency for given term."""
        if term not in self.index:
            return {}
        return {doc_id: len(positions) for doc_id, positions in self.index[term].items()}
        
    def get_document_frequency(self, term: str) -> int:
        return len(self.index.get(term, {}))
