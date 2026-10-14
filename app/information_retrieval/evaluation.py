import math
from typing import List, Dict

class InformationRetrievalEvaluator:
    """
    Evaluates IR ranking performance:
    - Precision@K
    - Recall@K
    - Reciprocal Rank (RR)
    - Mean Reciprocal Rank (MRR)
    - Normalized Discounted Cumulative Gain (NDCG@K)
    """
    
    @staticmethod
    def precision_at_k(retrieved_doc_ids: List[str], relevant_doc_ids: Set_or_List, k: int) -> float:
        top_k = retrieved_doc_ids[:k]
        if not top_k:
            return 0.0
        rel_set = set(relevant_doc_ids)
        hits = sum(1 for d in top_k if d in rel_set)
        return hits / k
        
    @staticmethod
    def recall_at_k(retrieved_doc_ids: List[str], relevant_doc_ids: List[str], k: int) -> float:
        rel_set = set(relevant_doc_ids)
        if not rel_set:
            return 0.0
        top_k = retrieved_doc_ids[:k]
        hits = sum(1 for d in top_k if d in rel_set)
        return hits / len(rel_set)
        
    @staticmethod
    def reciprocal_rank(retrieved_doc_ids: List[str], relevant_doc_ids: List[str]) -> float:
        rel_set = set(relevant_doc_ids)
        for rank, doc_id in enumerate(retrieved_doc_ids, start=1):
            if doc_id in rel_set:
                return 1.0 / rank
        return 0.0
        
    @classmethod
    def evaluate_query_benchmark(cls, query_eval_data: List[Dict]) -> dict:
        """
        query_eval_data is a list of dicts:
        [{'query': q, 'retrieved': [d1, d2...], 'relevant': [d1, d5]}]
        """
        p3_list, r3_list, rr_list = [], [], []
        
        for item in query_eval_data:
            p3 = cls.precision_at_k(item["retrieved"], item["relevant"], k=3)
            r3 = cls.recall_at_k(item["retrieved"], item["relevant"], k=3)
            rr = cls.reciprocal_rank(item["retrieved"], item["relevant"])
            
            p3_list.append(p3)
            r3_list.append(r3)
            rr_list.append(rr)
            
        return {
            "mean_precision_at_3": round(sum(p3_list) / max(1, len(p3_list)), 4),
            "mean_recall_at_3": round(sum(r3_list) / max(1, len(r3_list)), 4),
            "mrr": round(sum(rr_list) / max(1, len(rr_list)), 4),
            "queries_evaluated": len(query_eval_data)
        }
