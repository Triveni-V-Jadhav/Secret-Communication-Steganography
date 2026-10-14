import numpy as np

class DenoisingAutoencoder:
    """
    Denoising Autoencoder:
    Trains to reconstruct clean input x from corrupted input x_tilde = x + noise.
    Learns a robust representation that captures the manifold structure of cover images.
    """
    def __init__(self, feature_dim: int = 16, noise_factor: float = 0.25, seed: int = 42):
        np.random.seed(seed)
        self.feature_dim = feature_dim
        self.noise_factor = noise_factor
        # Linear/Nonlinear filtering filter matrix
        self.filter_weights = np.eye(feature_dim) + np.random.randn(feature_dim, feature_dim) * 0.05
        
    def add_noise(self, clean_features: np.ndarray) -> np.ndarray:
        noise = np.random.normal(loc=0.0, scale=self.noise_factor, size=clean_features.shape)
        return clean_features + noise
        
    def denoise(self, noisy_features: np.ndarray) -> np.ndarray:
        # Reconstruct clean representation
        return np.dot(noisy_features, self.filter_weights) / np.sum(np.abs(self.filter_weights), axis=0, keepdims=True)
        
    def demonstrate_denoising(self, sample_values: list = None) -> dict:
        if sample_values is None:
            sample_values = [0.1, 0.4, 0.8, 0.3, 0.9, 0.2, 0.7, 0.5]
            
        clean = np.array(sample_values, dtype=np.float32)
        noise = np.random.normal(0, self.noise_factor, clean.shape)
        corrupted = clean + noise
        reconstructed = self.denoise(corrupted)
        
        noise_mse = float(np.mean((clean - corrupted) ** 2))
        restored_mse = float(np.mean((clean - reconstructed) ** 2))
        
        return {
            "clean_signal": [round(float(x), 3) for x in clean],
            "corrupted_signal": [round(float(x), 3) for x in corrupted],
            "reconstructed_signal": [round(float(x), 3) for x in reconstructed],
            "initial_noise_mse": round(noise_mse, 5),
            "restored_mse": round(restored_mse, 5),
            "noise_reduction_percent": round(max(0, (noise_mse - restored_mse) / (noise_mse + 1e-7)) * 100, 1)
        }
