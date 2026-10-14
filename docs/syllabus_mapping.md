# Syllabus Mapping Document

## Syllabus 1: Deep Learning & Computer Vision

| Unit | Syllabus Topic | Implemented Module / File | Application UI Route | Demonstration / Integration |
|---|---|---|---|---|
| **Unit IV** | Sequence Learning Problem | `app/deep_learning/rnn_model.py` | `/deep-learning/rnn-lstm` | Multi-step communication sequence category prediction |
| **Unit IV** | Unfolding Computational Graphs | `docs/algorithms.md`, `rnn_model.py` | `/deep-learning/rnn-lstm` | Step-by-step unrolled graph diagram & BPTT formula |
| **Unit IV** | Recurrent Neural Network | `app/deep_learning/rnn_model.py` | `/deep-learning/rnn-lstm` | Forward recurrence with tanh activation & softmax outputs |
| **Unit IV** | Vanishing & Exploding Gradients | `docs/algorithms.md` | `/deep-learning/rnn-lstm` | Gradient clipping explanation & constant error carousel |
| **Unit IV** | Long Short-Term Memory (LSTM) | `app/deep_learning/lstm_model.py` | `/deep-learning/rnn-lstm` | Full gating equations: Forget, Input, Candidate, Output gates |
| **Unit IV** | Selective Read & Write | `app/deep_learning/lstm_model.py` | `/deep-learning/rnn-lstm` | Gate activation table tracking $f_t$, $i_t$, and $C_t$ |
| **Unit IV** | Self-Driving Cars Case Study | `app/deep_learning/lstm_model.py` | `/deep-learning/rnn-lstm` | Vehicle speed/steering trajectory simulator and coordinate forecast |
| **Unit V** | Autoencoder Architecture | `app/deep_learning/autoencoder.py` | `/deep-learning/autoencoders` | Symmetric bottleneck encoder/latent/decoder topology |
| **Unit V** | Denoising Autoencoder | `app/deep_learning/denoising_autoencoder.py`| `/deep-learning/autoencoders` | Gaussian noise corruption and manifold restoration |
| **Unit V** | Network Traffic Anomaly Detection | `app/deep_learning/anomaly_detection.py` | `/deep-learning/autoencoders` | 95th percentile threshold scoring of normal vs attack network flows |
| **Unit VI** | Facial Recognition & Biometrics | `app/face_recognition/` | `/auth/enroll-face`, `/messages/extract` | Haar cascade detection, 128D spatial template & cosine matching |

---

## Syllabus 2: Language Models & Information Retrieval

| Unit | Syllabus Topic | Implemented Module / File | Application UI Route | Demonstration / Integration |
|---|---|---|---|---|
| **Unit IV** | Language Models & Finite Automata | `app/nlp/language_model.py` | `/deep-learning/information-retrieval` | State-based tokenization & n-gram language models |
| **Unit IV** | Unigram & Bigram Language Models | `app/nlp/language_model.py` | `/deep-learning/information-retrieval` | Multinomial distributions with Add-Alpha Laplace smoothing |
| **Unit IV** | Query-Likelihood Ranking | `app/nlp/language_model.py` | `/deep-learning/information-retrieval` | $\log P(Q \mid D)$ ranking with Jelinek-Mercer background smoothing |
| **Unit V** | MapReduce Web Retrieval | `app/information_retrieval/ranking.py` | `/deep-learning/information-retrieval` | Map, Shuffle/Sort, and Reduce inverted index simulation |
| **Unit V** | PageRank (Link-Based Ranking) | `app/information_retrieval/ranking.py` | `/deep-learning/information-retrieval` | Power iteration on directed graph ($d = 0.85$) |
| **Unit V** | Safe Web Crawler | `app/information_retrieval/crawler.py` | `/analytics/web-crawler` | SSRF-safe crawling, allowlists, and BeautifulSoup4 parsing |
| **Unit VI** | Content-Based Recommenders | `app/information_retrieval/recommender.py`| `/analytics/recommender` | TF-IDF cosine similarity recommendations |
| **Unit VI** | Collaborative Filtering | `app/information_retrieval/recommender.py`| `/deep-learning/information-retrieval` | User-item rating matrix & item-item similarity |
| **Unit VI** | Knowledge-Based Recommenders | `app/information_retrieval/recommender.py`| `/analytics/recommender` | Constraint-based domain and skill matching |
| **Unit VI** | Text Extraction & NER | `app/nlp/message_analysis.py` | `/analytics/nlp-laboratory` | Tokenization, stopwords, and IP/email/crypto entity extraction |
