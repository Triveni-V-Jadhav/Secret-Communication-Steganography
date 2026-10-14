import numpy as np

class VanillaRNNCell:
    """
    Pedagogical implementation of a Vanilla Recurrent Neural Network forward step:
    h_t = tanh(W_xh * x_t + W_hh * h_{t-1} + b_h)
    y_t = softmax(W_hy * h_t + b_y)
    """
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, seed: int = 42):
        np.random.seed(seed)
        # Xavier/Glorot initialization
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        
        self.W_xh = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / (input_dim + hidden_dim))
        self.W_hh = np.random.randn(hidden_dim, hidden_dim) * np.sqrt(2.0 / (hidden_dim + hidden_dim))
        self.b_h = np.zeros((1, hidden_dim))
        
        self.W_hy = np.random.randn(hidden_dim, output_dim) * np.sqrt(2.0 / (hidden_dim + output_dim))
        self.b_y = np.zeros((1, output_dim))
        
    def forward(self, X_sequence: np.ndarray):
        """
        X_sequence: shape (T, input_dim)
        Returns:
            hidden_states: shape (T, hidden_dim)
            outputs: shape (T, output_dim)
        """
        T = X_sequence.shape[0]
        h_prev = np.zeros((1, self.hidden_dim))
        hidden_states = []
        outputs = []
        
        for t in range(T):
            x_t = X_sequence[t:t+1]
            # Recurrent linear transformation + non-linear tanh activation
            h_t = np.tanh(np.dot(x_t, self.W_xh) + np.dot(h_prev, self.W_hh) + self.b_h)
            y_t_logits = np.dot(h_t, self.W_hy) + self.b_y
            # Softmax
            exp_y = np.exp(y_t_logits - np.max(y_t_logits))
            y_t = exp_y / np.sum(exp_y)
            
            hidden_states.append(h_t[0])
            outputs.append(y_t[0])
            h_prev = h_t
            
        return np.array(hidden_states), np.array(outputs)

class EventSequencePredictor:
    """
    Analyzes sequences of communication events (e.g., login, encode, verify, download)
    to predict the next event category or detect anomalous workflow transitions.
    """
    CATEGORIES = ["AUTH_LOGIN", "ENCODE_INIT", "CHUNK_DOWNLOAD", "RECIPIENT_DECODE", "FACE_VERIFY", "MESSAGE_READ"]
    
    def __init__(self):
        self.cat_to_idx = {cat: i for i, cat in enumerate(self.CATEGORIES)}
        self.idx_to_cat = {i: cat for i, cat in enumerate(self.CATEGORIES)}
        self.rnn = VanillaRNNCell(input_dim=len(self.CATEGORIES), hidden_dim=8, output_dim=len(self.CATEGORIES))
        
    def one_hot(self, category_name: str) -> np.ndarray:
        vec = np.zeros(len(self.CATEGORIES))
        if category_name in self.cat_to_idx:
            vec[self.cat_to_idx[category_name]] = 1.0
        return vec
        
    def predict_next(self, sequence_events: list) -> dict:
        if not sequence_events:
            sequence_events = ["AUTH_LOGIN"]
        X_seq = np.array([self.one_hot(e) for e in sequence_events])
        h_states, outputs = self.rnn.forward(X_seq)
        
        last_pred_probs = outputs[-1]
        best_idx = int(np.argmax(last_pred_probs))
        
        return {
            "input_sequence": sequence_events,
            "predicted_next_event": self.idx_to_cat[best_idx],
            "confidence": round(float(last_pred_probs[best_idx]), 4),
            "class_probabilities": {self.idx_to_cat[i]: round(float(last_pred_probs[i]), 4) for i in range(len(self.CATEGORIES))},
            "num_timesteps": len(sequence_events)
        }
