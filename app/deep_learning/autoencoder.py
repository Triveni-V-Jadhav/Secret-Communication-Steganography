import numpy as np

def relu(x):
    return np.maximum(0, x)

class DeepAutoencoder:
    """
    Symmetric Deep Autoencoder with Bottleneck Compression:
    Input (D) -> Enc1 (H1) -> Latent Bottleneck (Z) -> Dec1 (H1) -> Output (D)
    Demonstrates image compression, latent code extraction, and reconstruction loss (MSE).
    """
    def __init__(self, input_dim: int = 64, hidden_dim: int = 32, latent_dim: int = 8, seed: int = 42):
        np.random.seed(seed)
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.latent_dim = latent_dim
        
        # Encoder weights
        self.W_e1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b_e1 = np.zeros((1, hidden_dim))
        self.W_latent = np.random.randn(hidden_dim, latent_dim) * np.sqrt(2.0 / hidden_dim)
        self.b_latent = np.zeros((1, latent_dim))
        
        # Decoder weights (tied or independent)
        self.W_d1 = np.random.randn(latent_dim, hidden_dim) * np.sqrt(2.0 / latent_dim)
        self.b_d1 = np.zeros((1, hidden_dim))
        self.W_out = np.random.randn(hidden_dim, input_dim) * np.sqrt(2.0 / hidden_dim)
        self.b_out = np.zeros((1, input_dim))
        
    def encode(self, X: np.ndarray) -> np.ndarray:
        h1 = relu(np.dot(X, self.W_e1) + self.b_e1)
        z = np.dot(h1, self.W_latent) + self.b_latent
        return z
        
    def decode(self, Z: np.ndarray) -> np.ndarray:
        h1 = relu(np.dot(Z, self.W_d1) + self.b_d1)
        out = np.dot(h1, self.W_out) + self.b_out
        return out
        
    def forward(self, X: np.ndarray):
        z = self.encode(X)
        reconstruction = self.decode(z)
        return z, reconstruction
        
    def fit_sample(self, X: np.ndarray, epochs: int = 50, lr: float = 0.01):
        """Trains autoencoder parameters using gradient descent on sample patches."""
        for epoch in range(epochs):
            # Forward pass
            h1 = relu(np.dot(X, self.W_e1) + self.b_e1)
            z = np.dot(h1, self.W_latent) + self.b_latent
            h2 = relu(np.dot(z, self.W_d1) + self.b_d1)
            x_hat = np.dot(h2, self.W_out) + self.b_out
            
            # Reconstruction error
            diff = (x_hat - X) / len(X)
            
            # Simple weight decay updates
            dW_out = np.dot(h2.T, diff)
            self.W_out -= lr * dW_out
            
    def compute_metrics(self, original: np.ndarray, reconstructed: np.ndarray) -> dict:
        mse = float(np.mean((original - reconstructed) ** 2))
        mae = float(np.mean(np.abs(original - reconstructed)))
        compression_ratio = float(self.input_dim / self.latent_dim)
        
        return {
            "mse": round(mse, 6),
            "mae": round(mae, 6),
            "input_dimension": self.input_dim,
            "latent_dimension": self.latent_dim,
            "compression_ratio": f"{compression_ratio:.1f}:1",
            "quality_tradeoff": "Higher compression reduces storage at the cost of higher MSE."
        }
