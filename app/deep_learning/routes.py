from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.deep_learning.rnn_model import EventSequencePredictor
from app.deep_learning.lstm_model import VehicleTrajectorySimulator
from app.deep_learning.autoencoder import DeepAutoencoder
from app.deep_learning.denoising_autoencoder import DenoisingAutoencoder
from app.deep_learning.anomaly_detection import NetworkTrafficAnomalyDetector
from app.nlp.language_model import NgramLanguageModel
from app.nlp.text_classification import TextCategoryClassifier
from app.nlp.message_analysis import MessageAnalyzer
from app.information_retrieval.crawler import SafeWebCrawler
from app.information_retrieval.ranking import PageRankEngine, MapReduceSimulation
from app.information_retrieval.recommender import EducationalRecommenderSystem
from app.face_recognition.evaluation import BiometricEvaluator

dl_bp = Blueprint("deep_learning", __name__, url_prefix="/deep-learning")

@dl_bp.route("/")
@login_required
def lab_index():
    return render_template("deep_learning/index.html")

@dl_bp.route("/rnn-lstm", methods=["GET", "POST"])
@login_required
def rnn_lstm_demo():
    predictor = EventSequencePredictor()
    sim = VehicleTrajectorySimulator()
    
    events = ["AUTH_LOGIN", "ENCODE_INIT", "CHUNK_DOWNLOAD"]
    if request.method == "POST":
        raw_events = request.form.get("events", "AUTH_LOGIN,ENCODE_INIT,CHUNK_DOWNLOAD")
        events = [e.strip() for e in raw_events.split(",") if e.strip()]
        
    rnn_result = predictor.predict_next(events)
    trajectory_result = sim.simulate_and_predict(num_timesteps=8)
    
    return render_template(
        "deep_learning/rnn_lstm.html",
        rnn_result=rnn_result,
        trajectory=trajectory_result,
        events_str=",".join(events)
    )

@dl_bp.route("/autoencoders", methods=["GET", "POST"])
@login_required
def autoencoder_demo():
    dae = DeepAutoencoder(input_dim=16, hidden_dim=8, latent_dim=4)
    denoiser = DenoisingAutoencoder(noise_factor=0.3)
    anomaly_detector = NetworkTrafficAnomalyDetector()
    
    denoise_res = denoiser.demonstrate_denoising([0.2, 0.8, 0.5, 0.9, 0.1, 0.6, 0.4, 0.7])
    
    # Anomaly test vector
    sample_flow = [12, 1600, 0.04, 11, 0.01]  # normal
    if request.method == "POST" and request.form.get("is_attack") == "true":
        sample_flow = [160, 99000, 0.88, 2, 0.45]  # anomalous
        
    anomaly_res = anomaly_detector.score_traffic(sample_flow)
    
    return render_template(
        "deep_learning/autoencoders.html",
        denoise=denoise_res,
        anomaly=anomaly_res,
        sample_flow=sample_flow
    )

@dl_bp.route("/information-retrieval", methods=["GET", "POST"])
@login_required
def ir_demo():
    sample_docs = {
        "doc1": "Steganography enables secret communication by hiding payloads within cover images.",
        "doc2": "AES-256 authenticated encryption ensures confidential transmission and prevents tampering.",
        "doc3": "Biometric face verification uses spatial feature vectors to verify identity with consent.",
        "doc4": "Deep autoencoders compress data and detect anomalous network intrusion flows."
    }
    
    lm = NgramLanguageModel()
    lm.fit(list(sample_docs.values()))
    
    query = request.args.get("q", "secret communication steganography")
    scores = {}
    for did, text in sample_docs.items():
        scores[did] = lm.score_query_likelihood(query, text)
        
    # PageRank synthetic graph
    graph = {
        "A_stego": ["B_crypto", "C_face"],
        "B_crypto": ["A_stego", "D_anomaly"],
        "C_face": ["A_stego"],
        "D_anomaly": ["B_crypto"]
    }
    pr_scores = PageRankEngine.compute_pagerank(graph)
    mr_res = MapReduceSimulation.execute_simulation(sample_docs)
    cf_res = EducationalRecommenderSystem.collaborative_filtering_demo()
    
    return render_template(
        "deep_learning/information_retrieval.html",
        docs=sample_docs,
        query=query,
        lm_scores=scores,
        pagerank=pr_scores,
        mapreduce=mr_res,
        collab=cf_res
    )

@dl_bp.route("/model-evaluations")
@login_required
def evaluations():
    # Biometric FAR / FRR evaluation curve
    genuine = [0.88, 0.92, 0.85, 0.79, 0.94, 0.82, 0.76, 0.89, 0.91]
    impostor = [0.32, 0.45, 0.51, 0.28, 0.62, 0.39, 0.41, 0.48, 0.35]
    bio_eval = BiometricEvaluator.evaluate_thresholds(genuine, impostor)
    
    return render_template("deep_learning/evaluations.html", bio_eval=bio_eval)
