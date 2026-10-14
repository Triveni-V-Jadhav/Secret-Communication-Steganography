import numpy as np
from typing import Dict, List

class PageRankEngine:
    """
    Second Syllabus Unit V: Link-Based Ranking (PageRank).
    Computes stationary distribution on directed hyperlink graphs:
    PR(u) = (1 - d) / N + d * \sum_{v \in In(u)} PR(v) / Out(v)
    where d = 0.85 (damping factor) and N = total nodes.
    """
    
    @staticmethod
    def compute_pagerank(graph: Dict[str, List[str]], damping: float = 0.85, max_iter: int = 40, tol: float = 1e-6) -> Dict[str, float]:
        """
        graph: adjacency dict where node -> list of outbound target nodes
        Returns: dict of node -> stationary PageRank score
        """
        nodes = sorted(list(graph.keys()))
        N = len(nodes)
        if N == 0:
            return {}
            
        node_to_idx = {n: i for i, n in enumerate(nodes)}
        
        # Build stochastic transition matrix M
        M = np.zeros((N, N), dtype=np.float64)
        for u, neighbors in graph.items():
            u_idx = node_to_idx[u]
            if len(neighbors) == 0:
                # Dangling node links uniformly to all nodes
                M[:, u_idx] = 1.0 / N
            else:
                weight = 1.0 / len(neighbors)
                for v in neighbors:
                    if v in node_to_idx:
                        v_idx = node_to_idx[v]
                        M[v_idx, u_idx] += weight
                        
        # Power iteration
        r = np.ones(N, dtype=np.float64) / N
        teleport = np.ones(N, dtype=np.float64) * ((1.0 - damping) / N)
        
        for iteration in range(max_iter):
            r_next = damping * np.dot(M, r) + teleport
            diff = np.linalg.norm(r_next - r, 1)
            r = r_next
            if diff < tol:
                break
                
        return {nodes[i]: round(float(r[i]), 5) for i in range(N)}

class MapReduceSimulation:
    """
    Second Syllabus Unit V: MapReduce Web Retrieval.
    Simulates Map, Shuffle/Sort, and Reduce phases for distributed indexing.
    """
    
    @staticmethod
    def map_phase(doc_id: str, text: str) -> List[tuple]:
        words = text.lower().split()
        return [(w, (doc_id, 1)) for w in words]
        
    @staticmethod
    def shuffle_sort(mapped_pairs: List[tuple]) -> Dict[str, List[tuple]]:
        grouped = {}
        for word, val in mapped_pairs:
            grouped.setdefault(word, []).append(val)
        return grouped
        
    @staticmethod
    def reduce_phase(grouped_pairs: Dict[str, List[tuple]]) -> Dict[str, Dict[str, int]]:
        inverted_postings = {}
        for word, doc_tuples in grouped_pairs.items():
            counts = {}
            for doc_id, count in doc_tuples:
                counts[doc_id] = counts.get(doc_id, 0) + count
            inverted_postings[word] = counts
        return inverted_postings
        
    @classmethod
    def execute_simulation(cls, sample_corpus: Dict[str, str]) -> dict:
        all_mapped = []
        for doc_id, text in sample_corpus.items():
            all_mapped.extend(cls.map_phase(doc_id, text))
            
        grouped = cls.shuffle_sort(all_mapped)
        reduced = cls.reduce_phase(grouped)
        
        return {
            "mapped_pairs_count": len(all_mapped),
            "unique_terms_reduced": len(reduced),
            "sample_index": {k: reduced[k] for k in list(reduced.keys())[:5]},
            "pipeline_stages": ["Map (Tokenization)", "Shuffle/Sort (Grouping by Key)", "Reduce (Aggregation to Postings)"]
        }
