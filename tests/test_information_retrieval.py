import pytest
from app.nlp.preprocessing import TextPreprocessor
from app.nlp.language_model import NgramLanguageModel
from app.nlp.text_classification import TextCategoryClassifier
from app.nlp.message_analysis import MessageAnalyzer
from app.information_retrieval.indexer import InvertedIndex
from app.information_retrieval.search import SearchEngine
from app.information_retrieval.crawler import SafeWebCrawler
from app.information_retrieval.ranking import PageRankEngine, MapReduceSimulation

def test_language_model_ranking():
    docs = [
        "Steganography hides messages in images.",
        "Cryptography encrypts text using secret algorithms."
    ]
    lm = NgramLanguageModel()
    lm.fit(docs)
    
    score1 = lm.score_query_likelihood("steganography images", docs[0])
    score2 = lm.score_query_likelihood("steganography images", docs[1])
    # Doc 1 should be ranked higher for this query
    assert score1 > score2

def test_inverted_index_and_search():
    index = InvertedIndex()
    index.add_document("d1", "Secret communication steganography system", {"title": "Doc 1"})
    index.add_document("d2", "Network anomaly detection using deep neural networks", {"title": "Doc 2"})
    
    engine = SearchEngine(index)
    results = engine.search_tfidf("steganography communication", top_k=2)
    assert len(results) > 0
    assert results[0]["doc_id"] == "d1"

def test_pagerank_computation():
    graph = {
        "A": ["B", "C"],
        "B": ["C"],
        "C": ["A"]
    }
    pr = PageRankEngine.compute_pagerank(graph)
    assert len(pr) == 3
    # Sum of PageRank scores across graph equals 1.0
    assert pytest.approx(sum(pr.values()), rel=1e-3) == 1.0

def test_crawler_ssrf_protection():
    # Loopback & private addresses must be strictly blocked
    assert SafeWebCrawler.is_safe_url("http://127.0.0.1/admin") is False
    assert SafeWebCrawler.is_safe_url("http://localhost:5000") is False
    assert SafeWebCrawler.is_safe_url("http://169.254.169.254/latest/meta-data/") is False
    assert SafeWebCrawler.is_safe_url("http://192.168.1.1/router") is False

def test_entity_extraction():
    text = "Audit on 2026-10-13 for 192.168.1.100. Contact: analyst@securecomm.local"
    entities = MessageAnalyzer.extract_named_entities(text)
    assert "EMAIL" in entities
    assert "IP_ADDRESS" in entities
    assert "analyst@securecomm.local" in entities["EMAIL"]
