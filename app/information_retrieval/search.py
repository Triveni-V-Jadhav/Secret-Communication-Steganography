import math
from typing import List, Dict
from app.nlp.preprocessing import TextPreprocessor
from app.information_retrieval.indexer import InvertedIndex

class SearchEngine:
    """
    Search engine supporting TF-IDF vector space ranking,
    cosine similarity, and authorization filtering.
    """
    
    def __init__(self, index: InvertedIndex):
        self.index = index
        
    def search_tfidf(self, query: str, top_k: int = 5) -> List[Dict]:
        query_terms = TextPreprocessor.tokenize(query)
        if not query_terms or self.index.total_docs == 0:
            return []
            
        N = self.index.total_docs
        scores = {}
        
        for term in query_terms:
            df = self.index.get_document_frequency(term)
            if df == 0:
                continue
            # Standard smoothed IDF
            idf = math.log((N + 1) / (df + 1)) + 1.0
            postings = self.index.get_postings(term)
            
            for doc_id, tf in postings.items():
                doc_len = max(1, self.index.doc_lengths.get(doc_id, 1))
                norm_tf = tf / doc_len
                score = norm_tf * idf
                scores[doc_id] = scores.get(doc_id, 0.0) + score
                
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_id, score in ranked:
            meta = self.index.doc_metadata.get(doc_id, {})
            results.append({
                "doc_id": doc_id,
                "score": round(score, 4),
                "title": meta.get("title", doc_id),
                "snippet": meta.get("snippet", ""),
                "is_knowledge_base": meta.get("is_knowledge_base", True)
            })
            
        return results
