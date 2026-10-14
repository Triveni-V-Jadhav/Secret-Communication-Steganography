from typing import List, Dict
from app.nlp.preprocessing import TextPreprocessor

class PassageRetriever:
    """
    Passage Retrieval: Splits large documents into overlapping passages (e.g. 50 words with 15 word stride)
    and retrieves the most relevant passage for fine-grained information retrieval.
    """
    
    @staticmethod
    def chunk_into_passages(text: str, window_size: int = 40, stride: int = 20) -> List[Dict]:
        words = text.split()
        passages = []
        
        for i in range(0, len(words), stride):
            window = words[i : i + window_size]
            if not window:
                break
            passages.append({
                "passage_id": f"p_{i}",
                "start_token": i,
                "text": " ".join(window)
            })
            if i + window_size >= len(words):
                break
                
        return passages
        
    @classmethod
    def retrieve_best_passage(cls, query: str, document_text: str) -> dict:
        passages = cls.chunk_into_passages(document_text)
        if not passages:
            return {"passage": "", "score": 0.0}
            
        q_tokens = set(TextPreprocessor.tokenize(query))
        best_p = passages[0]["text"]
        best_score = 0
        
        for p in passages:
            p_tokens = set(TextPreprocessor.tokenize(p["text"]))
            overlap = len(q_tokens.intersection(p_tokens))
            if overlap > best_score:
                best_score = overlap
                best_p = p["text"]
                
        return {
            "best_passage": best_p,
            "term_overlap_score": best_score,
            "total_passages_evaluated": len(passages)
        }
