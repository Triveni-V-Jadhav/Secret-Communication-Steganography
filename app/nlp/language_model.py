import math
from collections import Counter
from typing import List, Dict
from app.nlp.preprocessing import TextPreprocessor

class NgramLanguageModel:
    """
    Second Syllabus Unit IV: Language Models for Information Retrieval.
    Implements Unigram and Bigram Language Models with Laplace (Add-1) / Jelinek-Mercer Smoothing
    and Multinomial Word Distributions.
    """
    
    def __init__(self, smoothing_alpha: float = 0.5):
        self.alpha = smoothing_alpha
        self.unigram_counts = Counter()
        self.bigram_counts = Counter()
        self.total_tokens = 0
        self.vocabulary = set()
        
    def fit(self, corpus_documents: List[str]):
        """Estimates multinomial word distributions from documents."""
        self.unigram_counts.clear()
        self.bigram_counts.clear()
        self.vocabulary.clear()
        self.total_tokens = 0
        
        for doc in corpus_documents:
            tokens = TextPreprocessor.tokenize(doc)
            if not tokens:
                continue
            self.total_tokens += len(tokens)
            self.unigram_counts.update(tokens)
            self.vocabulary.update(tokens)
            
            # Bigrams
            for i in range(len(tokens) - 1):
                bg = (tokens[i], tokens[i+1])
                self.bigram_counts[bg] += 1
                
    def unigram_probability(self, word: str) -> float:
        """Maximum Likelihood with Add-Alpha Smoothing."""
        V = max(1, len(self.vocabulary))
        count = self.unigram_counts.get(word, 0)
        return (count + self.alpha) / (self.total_tokens + self.alpha * V)
        
    def bigram_probability(self, w1: str, w2: str) -> float:
        """P(w2 | w1) with Add-Alpha Smoothing."""
        V = max(1, len(self.vocabulary))
        bg_count = self.bigram_counts.get((w1, w2), 0)
        w1_count = self.unigram_counts.get(w1, 0)
        return (bg_count + self.alpha) / (w1_count + self.alpha * V)
        
    def score_query_likelihood(self, query: str, document_text: str) -> float:
        """
        Query-Likelihood Ranking model:
        Scores P(Q | D) = \prod_{w \in Q} [(1 - \lambda) * P_ml(w | D) + \lambda * P_ml(w | C)]
        using log-likelihood.
        """
        doc_tokens = TextPreprocessor.tokenize(document_text)
        doc_len = len(doc_tokens)
        if doc_len == 0:
            return -999.0
            
        doc_counts = Counter(doc_tokens)
        query_tokens = TextPreprocessor.tokenize(query)
        lambda_param = 0.3  # Background collection smoothing weight
        
        log_prob = 0.0
        for qw in query_tokens:
            p_doc = doc_counts.get(qw, 0) / doc_len
            p_coll = self.unigram_probability(qw)
            p_smoothed = (1.0 - lambda_param) * p_doc + lambda_param * p_coll
            log_prob += math.log(max(1e-9, p_smoothed))
            
        return round(log_prob, 4)
