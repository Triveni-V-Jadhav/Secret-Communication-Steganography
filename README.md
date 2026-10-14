# Secret Communication Using Multi-Image Steganography and Face Recognition
**MCA Major Academic Project**

[![Tests: Passing](https://img.shields.io/badge/Tests-21%20Passed-success)]()
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)]()
[![Security: AES--256--GCM](https://img.shields.io/badge/Security-AES--256--GCM-red)]()

A full-stack cybersecurity, deep learning, computer vision, and information retrieval platform for confidential data exchange hidden across multiple image carriers.

---

## 1. Key Architectural Features

- **Multi-Image Steganography Engine:** Splits encrypted payloads across multiple lossless cover images (PNG/BMP) using a versioned 32-byte binary header (`SEC1`) and bitwise LSB plane manipulation.
- **Authenticated AES-256-GCM Encryption:** Employs PBKDF2-HMAC-SHA256 (100,000 iterations), random 96-bit nonces, and 128-bit authentication tags to prevent tampering and eavesdropping.
- **Privacy-Conscious Biometric Face Verification:** Utilizes OpenCV Haar cascades for single-face detection and 128-dimensional spatial-gradient feature vectors. Enforces explicit voluntary user consent and never stores raw facial photographs.
- **Deep Learning Laboratories (MCA Units IV & V):**
  - Unrolled Recurrent Neural Networks (RNN) for communication sequence classification.
  - Long Short-Term Memory (LSTM) with forget/input/output gating and vehicle trajectory time-series modeling (Self-Driving Cars Case Study).
  - Deep Autoencoders for image compression and Denoising Autoencoders for manifold reconstruction.
  - Network Traffic Cyber Anomaly Detection with 95th-percentile reconstruction error thresholds.
- **Language Models & Information Retrieval (MCA Units IV, V & VI):**
  - Unigram/Bigram multinomial distributions with Laplace and Jelinek-Mercer background smoothing.
  - Query-Likelihood scoring and passage retrieval.
  - Safe Web Crawler with strict SSRF defense (blocking private subnets and localhost) and BeautifulSoup4 parsing.
  - Link-based PageRank calculation on directed web graphs.
  - MapReduce inverted indexing simulation (Map $\rightarrow$ Shuffle $\rightarrow$ Reduce).
  - Tri-paradigm Recommender System (Content-based, Collaborative filtering, and Knowledge-based rules).

---

## 2. Directory Structure

```
secret_communication/
├── run.py                       # Main application startup entry point
├── config.py                    # Environment & application settings
├── requirements.txt             # Project dependencies
├── .env.example                 # Safe environment variable template
├── setup_windows.bat            # Automated Windows one-click installer
├── run_windows.bat              # Automated Windows web server runner
├── test_windows.bat             # Automated Windows pytest test suite runner
│
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── extensions.py            # SQLAlchemy, Flask-Login, CSRF, Migrate
│   ├── models/                  # Database models (User, Message, StegoImage, etc.)
│   ├── auth/                    # Registration, login, profile, and face enrollment
│   ├── communication/           # Steganography package creation, download, & extraction
│   ├── steganography/           # SEC1 encoder, decoder, validator, & payload manager
│   ├── face_recognition/        # Detection, spatial features, cosine similarity, & ROC eval
│   ├── cryptography/            # AES-256-GCM, PBKDF2 key derivation, and HMAC signatures
│   ├── deep_learning/           # RNN, LSTM, Autoencoder, DAE, Anomaly Detection labs
│   ├── nlp/                     # Tokenizer, stop words, N-gram LMs, text classifier, & NER
│   ├── information_retrieval/   # Inverted index, TF-IDF search, crawler, PageRank, MapReduce
│   ├── analytics/               # NLP, crawler, and recommendation routes
│   ├── security/                # Permissions, audit logging, and input sanitization
│   └── templates/               # Reusable Jinja2 templates (Dark cybersecurity theme)
│
├── datasets/sample_data/        # Sample lossless PNG cover images
├── scripts/
│   └── generate_demo_data.py    # Generates cover images and seeds demo users
├── tests/                       # Complete 21-scenario automated pytest suite
└── docs/                        # Architecture, algorithms, security, and syllabus mappings
```

---

## 3. Quickstart & Execution (Windows)

### Step 1: Open PowerShell / Command Prompt
Navigate to the project directory:
```powershell
cd C:\Users\Sakshi\.gemini\antigravity\scratch\secret_communication
```

### Step 2: Automated Installation
Run the provided Windows setup script:
```cmd
setup_windows.bat
```
*Or manually:*
```powershell
pip install -r requirements.txt
pip install email-validator
python scripts\generate_demo_data.py
```

### Step 3: Run the Automated Test Suite
```powershell
python -m pytest tests -v
```
All 21 test scenarios will execute and pass.

### Step 4: Launch the Web Application
```powershell
python run.py
```
Open your web browser and navigate to:
**`http://127.0.0.1:5000`**

---

## 4. Default Seeded Demonstration Credentials

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Administrator** | `admin` | `AdminSecure2026!` | Administrative auditing & oversight |
| **Sender User** | `alice` | `AliceSecure2026!` | Secret package creation & encoding |
| **Recipient User** | `bob` | `BobSecure2026!` | Extraction, biometric probe & decryption |

---

## 5. Academic Syllabus Mapping

Full cross-reference documentation mapping each MCA syllabus unit and topic to its implemented code files and interactive user-facing screens is available in [`docs/syllabus_mapping.md`](docs/syllabus_mapping.md).
