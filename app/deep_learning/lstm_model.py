import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -15, 15)))

class LSTMCell:
    """
    Long Short-Term Memory (LSTM) Cell.
    Full gating mechanism:
    f_t = sigmoid(W_f [x_t, h_{t-1}] + b_f)  (Forget Gate)
    i_t = sigmoid(W_i [x_t, h_{t-1}] + b_i)  (Input Gate)
    c~_t = tanh(W_c [x_t, h_{t-1}] + b_c)    (Candidate Cell State)
    c_t = f_t * c_{t-1} + i_t * c~_t         (Cell State Update)
    o_t = sigmoid(W_o [x_t, h_{t-1}] + b_o)  (Output Gate)
    h_t = o_t * tanh(c_t)                    (Hidden State)
    """
    def __init__(self, input_dim: int, hidden_dim: int, seed: int = 42):
        np.random.seed(seed)
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        concat_dim = input_dim + hidden_dim
        
        # Combined weights for forget, input, candidate, output gates
        self.W_f = np.random.randn(concat_dim, hidden_dim) * 0.1
        self.b_f = np.ones((1, hidden_dim))  # Initial forget bias = 1 to preserve memory early
        
        self.W_i = np.random.randn(concat_dim, hidden_dim) * 0.1
        self.b_i = np.zeros((1, hidden_dim))
        
        self.W_c = np.random.randn(concat_dim, hidden_dim) * 0.1
        self.b_c = np.zeros((1, hidden_dim))
        
        self.W_o = np.random.randn(concat_dim, hidden_dim) * 0.1
        self.b_o = np.zeros((1, hidden_dim))
        
    def forward(self, X_seq: np.ndarray):
        """
        X_seq: shape (T, input_dim)
        Returns:
            h_states: list of h_t
            c_states: list of c_t
            gate_activations: list of dicts with (f, i, c_tilde, o) for educational visualization
        """
        T = X_seq.shape[0]
        h_prev = np.zeros((1, self.hidden_dim))
        c_prev = np.zeros((1, self.hidden_dim))
        
        h_states, c_states, gates = [], [], []
        
        for t in range(T):
            x_t = X_seq[t:t+1]
            concat = np.hstack([x_t, h_prev])
            
            f_t = sigmoid(np.dot(concat, self.W_f) + self.b_f)
            i_t = sigmoid(np.dot(concat, self.W_i) + self.b_i)
            c_tilde = np.tanh(np.dot(concat, self.W_c) + self.b_c)
            
            # Selective update
            c_t = f_t * c_prev + i_t * c_tilde
            o_t = sigmoid(np.dot(concat, self.W_o) + self.b_o)
            h_t = o_t * np.tanh(c_t)
            
            h_states.append(h_t[0].copy())
            c_states.append(c_t[0].copy())
            gates.append({
                "timestep": t,
                "forget_gate": float(np.mean(f_t)),
                "input_gate": float(np.mean(i_t)),
                "candidate_state": float(np.mean(c_tilde)),
                "output_gate": float(np.mean(o_t)),
                "cell_state_mean": float(np.mean(c_t)),
                "hidden_state_mean": float(np.mean(h_t))
            })
            
            h_prev, c_prev = h_t, c_t
            
        return np.array(h_states), np.array(c_states), gates

class VehicleTrajectorySimulator:
    """
    Unit IV Self-Driving Cars Educational Case Study:
    Demonstrates how an LSTM models vehicle sensor trajectories (speed, steering angle, acceleration)
    over time steps to forecast future trajectory displacement and lane alignment.
    """
    
    def __init__(self):
        # 3 sensor inputs: speed (m/s), steering_angle (rad), acceleration (m/s^2)
        self.lstm = LSTMCell(input_dim=3, hidden_dim=6, seed=123)
        self.W_out = np.random.randn(6, 2) * 0.2  # Predicts (delta_x, delta_y) displacement
        
    def simulate_and_predict(self, num_timesteps: int = 10) -> dict:
        # Generate synthetic smooth trajectory measurements
        t = np.linspace(0, 2 * np.pi, num_timesteps)
        speeds = 15.0 + 2.0 * np.sin(t)          # 13 to 17 m/s (~50 km/h)
        steering = 0.05 * np.cos(t)               # slight turns
        accel = 0.5 * np.cos(2 * t)
        
        sensors = np.column_stack([speeds, steering, accel])
        h_states, c_states, gates = self.lstm.forward(sensors)
        
        # Predict 2D displacement for each step
        displacements = np.dot(h_states, self.W_out)
        
        trajectory_points = []
        cur_x, cur_y = 0.0, 0.0
        for i in range(num_timesteps):
            cur_x += float(displacements[i, 0])
            cur_y += float(displacements[i, 1]) + (speeds[i] * 0.1)  # forward vehicle velocity
            trajectory_points.append({
                "step": i + 1,
                "speed": round(float(speeds[i]), 2),
                "steering": round(float(steering[i]), 4),
                "predicted_x": round(cur_x, 2),
                "predicted_y": round(cur_y, 2)
            })
            
        return {
            "trajectory": trajectory_points,
            "gate_activations": gates,
            "description": "LSTM vehicle trajectory tracking modeling dynamic temporal dependencies."
        }
