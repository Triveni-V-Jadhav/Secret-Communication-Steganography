from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from app.nlp.message_analysis import MessageAnalyzer
from app.nlp.text_classification import TextCategoryClassifier
from app.information_retrieval.crawler import SafeWebCrawler
from app.information_retrieval.recommender import EducationalRecommenderSystem

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.route("/")
@login_required
def index():
    return render_template("analytics/index.html")

@analytics_bp.route("/nlp-laboratory", methods=["GET", "POST"])
@login_required
def nlp_lab():
    text = "Security report for host 192.168.1.50: Detected potential cryptographic key mismatch on 2026-10-13. Contact security@example.com."
    if request.method == "POST":
        text = request.form.get("text", text)
        
    analysis = MessageAnalyzer.analyze_text(text)
    classifier = TextCategoryClassifier()
    classification = classifier.predict(text)
    
    return render_template(
        "analytics/nlp_lab.html",
        text=text,
        analysis=analysis,
        classification=classification
    )

@analytics_bp.route("/web-crawler", methods=["GET", "POST"])
@login_required
def crawler_demo():
    url = "https://example.com"
    crawl_result = None
    
    # Safe offline HTML parsing sample
    sample_html = """
    <html>
        <head><title>Secure Information Retrieval Knowledge Base</title></head>
        <body>
            <h1>Steganography and Cybersecurity Documentation</h1>
            <p>Welcome to the educational security repository. This article discusses multi-image LSB encoding and AES-GCM encryption.</p>
            <a href="https://example.com/crypto">Cryptographic Standards</a>
            <a href="https://example.com/face">Biometric Authentication</a>
        </body>
    </html>
    """
    
    if request.method == "POST":
        url = request.form.get("url", url).strip()
        is_safe = SafeWebCrawler.is_safe_url(url)
        if not is_safe:
            flash(f"Security Alert: Target URL '{url}' violates crawler safety policies (SSRF mitigation or domain allowlist).", "danger")
        else:
            crawl_result = SafeWebCrawler.parse_local_html(sample_html, source_url=url)
            flash("Parsing executed under strict security controls.", "success")
    else:
        crawl_result = SafeWebCrawler.parse_local_html(sample_html, source_url="https://example.com")
        
    return render_template("analytics/crawler.html", url=url, crawl_result=crawl_result)

@analytics_bp.route("/recommender", methods=["GET", "POST"])
@login_required
def recommender_view():
    skill = request.form.get("skill_level", "intermediate")
    domain = request.form.get("domain", "security")
    
    recommendations = EducationalRecommenderSystem.knowledge_based_recommend(skill, domain)
    return render_template(
        "analytics/recommender.html",
        recommendations=recommendations,
        skill=skill,
        domain=domain
    )
