import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from PIL import Image, ImageDraw
from app import create_app, db
from app.models import User, Message, StegoImage, Document, FaceProfile

def generate_sample_cover_images():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "datasets", "sample_data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate 3 distinct colorful lossless PNG cover images
    configs = [
        ("cover_scenery.png", (200, 200), (30, 144, 255)),     # Dodger blue
        ("cover_nature.png", (220, 220), (34, 139, 34)),       # Forest green
        ("cover_abstract.png", (180, 180), (220, 20, 60))      # Crimson
    ]
    
    for filename, size, color in configs:
        path = os.path.join(data_dir, filename)
        img = Image.new("RGB", size, color=color)
        draw = ImageDraw.Draw(img)
        # Draw some patterns to give variation
        draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(255, 255, 255), width=3)
        draw.ellipse([40, 40, size[0]-40, size[1]-40], fill=(color[0]//2, color[1]//2, color[2]//2))
        img.save(path, format="PNG")
        print(f"Generated sample cover image: {path} ({size[0]}x{size[1]})")

def seed_database():
    app = create_app("development")
    with app.app_context():
        db.create_all()
        
        # Create default Admin & Users if not existing
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@securecomm.local", role="ADMIN")
            admin.set_password("AdminSecure2026!")
            db.session.add(admin)
            print("Seeded Admin user: admin / AdminSecure2026!")
            
        if not User.query.filter_by(username="alice").first():
            alice = User(username="alice", email="alice@securecomm.local", role="USER")
            alice.set_password("AliceSecure2026!")
            db.session.add(alice)
            print("Seeded User: alice / AliceSecure2026!")
            
        if not User.query.filter_by(username="bob").first():
            bob = User(username="bob", email="bob@securecomm.local", role="USER")
            bob.set_password("BobSecure2026!")
            db.session.add(bob)
            print("Seeded User: bob / BobSecure2026!")
            
        db.session.commit()
        print("Database initialized and demo accounts created successfully!")

if __name__ == "__main__":
    generate_sample_cover_images()
    seed_database()
