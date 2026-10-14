import os
from app import create_app, db
from app.models import User, Message, StegoImage, FaceProfile, Document, AuditLog

app = create_app(os.getenv("FLASK_ENV", "development"))

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Message": Message,
        "StegoImage": StegoImage,
        "FaceProfile": FaceProfile,
        "Document": Document,
        "AuditLog": AuditLog
    }

if __name__ == "__main__":
    # Create tables if not present on direct startup
    with app.app_context():
        db.create_all()
    print("="*70)
    print("Secret Communication Web Application Initialized Successfully")
    print("Point your browser to: http://127.0.0.1:5000")
    print("="*70)
    app.run(host="127.0.0.1", port=5000, debug=True)
