import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-development-only-change-in-prod")
    
    # Database
    db_path = (BASE_DIR / "instance" / "application.db").resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File handling & uploads
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", 32)) * 1024 * 1024  # 32 MB limit
    UPLOAD_FOLDER = BASE_DIR / os.getenv("UPLOAD_FOLDER", "storage/uploads")
    STEGO_FOLDER = BASE_DIR / os.getenv("STEGO_FOLDER", "storage/stego_images")
    TEMP_FOLDER = BASE_DIR / os.getenv("TEMP_FOLDER", "storage/temporary")
    DATASET_FOLDER = BASE_DIR / "datasets" / "sample_data"
    MODELS_FOLDER = BASE_DIR / "trained_models"
    
    # Security & Sessions
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in ("true", "1", "t")
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # WTForms / CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Biometrics & ML parameters
    FACE_MATCH_THRESHOLD = float(os.getenv("FACE_MATCH_THRESHOLD", 0.72))
    ANOMALY_PERCENTILE_THRESHOLD = 95.0

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
