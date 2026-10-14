import numpy as np

class NetworkTrafficAnomalyDetector:
    """
    Autoencoder-based Anomaly Detection on synthetic network flow vectors:
    [packet_count, byte_rate, syn_flag_ratio, duration, error_rate]
    Normal traffic trains the autoencoder; anomalous intrusions yield high reconstruction errors.
    """
    
    def __init__(self, feature_dim: int = 5, latent_dim: int = 2, seed: int = 42):
        np.random.seed(seed)
        self.feature_dim = feature_dim
        self.latent_dim = latent_dim
        
        # Encoder & Decoder
        self.W_enc = np.random.randn(feature_dim, latent_dim) * 0.2
        self.b_enc = np.zeros(latent_dim)
        self.W_dec = np.random.randn(latent_dim, feature_dim) * 0.2
        self.b_dec = np.zeros(feature_dim)
        
        self.reconstruction_threshold = 0.45  # Documented threshold from normal validation validation set
        
    def fit_normal_baseline(self, normal_flows: np.ndarray):
        """Calculates reconstruction threshold at 95th percentile of normal traffic."""
        errors = self.calculate_errors(normal_flows)
        self.reconstruction_threshold = float(np.percentile(errors, 95))
        return self.reconstruction_threshold
        
    def forward(self, X: np.ndarray) -> np.ndarray:
        z = np.tanh(np.dot(X, self.W_enc) + self.b_enc)
        reconstruction = np.dot(z, self.W_dec) + self.b_dec
        return reconstruction
        
    def calculate_errors(self, flows: np.ndarray) -> np.ndarray:
        recon = self.forward(flows)
        # Mean Squared Error per sample row
        return np.mean((flows - recon) ** 2, axis=1)
        
    def score_traffic(self, flow_vector: list) -> dict:
        x = np.array([flow_vector], dtype=np.float32)
        error = float(self.calculate_errors(x)[0])
        is_anomalous = error > self.reconstruction_threshold
        
        return {
            "flow_vector": flow_vector,
            "reconstruction_error": round(error, 5),
            "threshold": round(self.reconstruction_threshold, 5),
            "is_anomaly": bool(is_anomalous),
            "threat_classification": "SUSPICIOUS_ANOMALY" if is_anomalous else "NORMAL_TRAFFIC",
            "confidence": round(min(1.0, error / (self.reconstruction_threshold * 2)), 3)
        }

    @staticmethod
    def generate_demo_dataset():
        """Generates synthetic normal and attack flows for educational benchmarking."""
        np.random.seed(101)
        # 100 normal flows centered around [10, 1500, 0.05, 12, 0.01]
        normal = np.random.normal(loc=[10, 1500, 0.05, 12, 0.01], scale=[2, 200, 0.02, 3, 0.005], size=(100, 5))
        # 20 anomalous flows (e.g. SYN Flood or Exfiltration burst: high syn ratio, huge byte rate)
        attack = np.random.normal(loc=[150, 95000, 0.85, 2, 0.40], scale=[20, 10000, 0.05, 1, 0.05], size=(20, 5))
        return normal, attack
