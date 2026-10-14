import pytest
import numpy as np
from app.deep_learning.rnn_model import VanillaRNNCell, EventSequencePredictor
from app.deep_learning.lstm_model import LSTMCell, VehicleTrajectorySimulator
from app.deep_learning.autoencoder import DeepAutoencoder
from app.deep_learning.denoising_autoencoder import DenoisingAutoencoder
from app.deep_learning.anomaly_detection import NetworkTrafficAnomalyDetector

def test_rnn_forward_pass():
    cell = VanillaRNNCell(input_dim=4, hidden_dim=6, output_dim=4)
    X = np.random.randn(5, 4)  # 5 timesteps
    h_states, outputs = cell.forward(X)
    assert h_states.shape == (5, 6)
    assert outputs.shape == (5, 4)
    # Check probabilities sum to 1.0
    for prob in outputs:
        assert np.isclose(np.sum(prob), 1.0)

def test_event_sequence_predictor():
    predictor = EventSequencePredictor()
    res = predictor.predict_next(["AUTH_LOGIN", "ENCODE_INIT"])
    assert "predicted_next_event" in res
    assert res["predicted_next_event"] in EventSequencePredictor.CATEGORIES

def test_lstm_forward_and_trajectory():
    sim = VehicleTrajectorySimulator()
    res = sim.simulate_and_predict(num_timesteps=6)
    assert len(res["trajectory"]) == 6
    assert len(res["gate_activations"]) == 6
    # Forget and input gates are within (0, 1)
    for gate in res["gate_activations"]:
        assert 0.0 <= gate["forget_gate"] <= 1.0
        assert 0.0 <= gate["input_gate"] <= 1.0

def test_deep_autoencoder():
    dae = DeepAutoencoder(input_dim=16, hidden_dim=8, latent_dim=4)
    X = np.random.randn(10, 16)
    z, recon = dae.forward(X)
    assert z.shape == (10, 4)
    assert recon.shape == (10, 16)
    metrics = dae.compute_metrics(X, recon)
    assert "mse" in metrics
    assert metrics["compression_ratio"] == "4.0:1"

def test_anomaly_detection_scoring():
    detector = NetworkTrafficAnomalyDetector()
    normal_flow = [10, 1500, 0.05, 12, 0.01]
    attack_flow = [180, 99000, 0.90, 2, 0.50]
    
    score_normal = detector.score_traffic(normal_flow)
    score_attack = detector.score_traffic(attack_flow)
    
    # Attack error should be higher than normal error
    assert score_attack["reconstruction_error"] > score_normal["reconstruction_error"]
