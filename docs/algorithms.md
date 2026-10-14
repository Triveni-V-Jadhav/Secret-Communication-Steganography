# Algorithmic Explanations and Mathematical Foundations

## 1. Multi-Image LSB Steganography
Least Significant Bit (LSB) steganography modifies the lowest-order bit of individual color byte values (0–255) across RGB channels.
Let pixel channel value be $P$. To embed bit $b \in \{0, 1\}$:
$$P' = (P \ \& \ \sim 1) \ | \ b$$
The visual impact is at most $\pm 1$ intensity level out of 256, rendering alterations invisible to the human eye.
**Capacity Calculation:**
$$\text{Capacity (bytes)} = \frac{W \times H \times 3}{8}$$

## 2. Long Short-Term Memory (LSTM)
Overcomes the vanishing gradient problem in vanilla RNNs through constant error carousels:
1. **Forget Gate:** $f_t = \sigma(W_f [x_t, h_{t-1}] + b_f)$
2. **Input Gate:** $i_t = \sigma(W_i [x_t, h_{t-1}] + b_i)$
3. **Candidate Cell State:** $\tilde{C}_t = \tanh(W_c [x_t, h_{t-1}] + b_c)$
4. **Cell State Update:** $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$
5. **Output Gate:** $o_t = \sigma(W_o [x_t, h_{t-1}] + b_o)$
6. **Hidden State:** $h_t = o_t \odot \tanh(C_t)$

## 3. Autoencoder & Reconstruction Error
Maps input $x \in \mathbb{R}^D$ to lower-dimensional latent space $z \in \mathbb{R}^d$ ($d \ll D$), then decodes $\hat{x} \in \mathbb{R}^D$.
$$\text{Reconstruction Error (MSE)} = \frac{1}{D} \sum_{i=1}^D (x_i - \hat{x}_i)^2$$
For network flow anomaly detection, flow samples exceeding the 95th percentile threshold $\tau$ are classified as malicious intrusions.

## 4. Query-Likelihood Language Model Ranking
Estimates probability that document $D$ generated query $Q = \{q_1, \dots, q_m\}$ using Jelinek-Mercer background smoothing:
$$\log P(Q \mid D) = \sum_{i=1}^m \log \left[ (1 - \lambda) \frac{c(q_i; D)}{|D|} + \lambda P(q_i \mid C) \right]$$

## 5. PageRank (Link-Based Ranking)
Stationary probability of a random web surfer with damping factor $d = 0.85$:
$$PR(u) = \frac{1 - d}{N} + d \sum_{v \in \text{In}(u)} \frac{PR(v)}{\text{Out}(v)}$$
