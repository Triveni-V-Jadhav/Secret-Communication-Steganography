import os
import uuid
import json
import zipfile
import io
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, current_app, abort, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.user import User
from app.models.message import Message
from app.models.stego_image import StegoImage
from app.models.audit_log import AuditLog
from app.cryptography.encryption import CryptoService
from app.steganography.encoder import StegoEncoder
from app.steganography.decoder import StegoDecoder
from app.steganography.payload_manager import PayloadManager
from app.steganography.image_validation import ImageValidator
from app.face_recognition.verification import FaceVerificationService
from app.security.permissions import AuditLogService

comm_bp = Blueprint("communication", __name__)

@comm_bp.route("/")
def index():
    return render_template("landing.html")

@comm_bp.route("/dashboard")
@login_required
def dashboard():
    sent_count = Message.query.filter_by(sender_id=current_user.id).count()
    recv_count = Message.query.filter_by(recipient_id=current_user.id).count()
    recent_sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).limit(5).all()
    recent_recv = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.created_at.desc()).limit(5).all()
    
    return render_template(
        "dashboard/dashboard.html",
        sent_count=sent_count,
        recv_count=recv_count,
        recent_sent=recent_sent,
        recent_recv=recent_recv
    )

@comm_bp.route("/messages/new", methods=["GET", "POST"])
@login_required
def create_message():
    users = User.query.filter(User.id != current_user.id, User.is_active == True).all()
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        recipient_id = request.form.get("recipient_id")
        secret_text = request.form.get("secret_message", "").strip()
        passphrase = request.form.get("passphrase", "").strip()
        require_face = request.form.get("require_face_auth") == "on"
        cover_files = request.files.getlist("cover_images")
        
        if not title or not secret_text or not passphrase:
            flash("Title, secret message, and encryption passphrase are required.", "danger")
            return render_template("communication/create_message.html", users=users)
            
        if not cover_files or len(cover_files) == 0 or cover_files[0].filename == "":
            flash("Please upload at least one cover image (lossless PNG format).", "danger")
            return render_template("communication/create_message.html", users=users)
            
        num_images = len(cover_files)
        msg_uuid = str(uuid.uuid4())
        
        # 1. Structure the secret payload (supports plain text + optional attached filename)
        payload_dict = {
            "uuid": msg_uuid,
            "title": title,
            "timestamp": datetime.utcnow().isoformat(),
            "content": secret_text,
            "sender_username": current_user.username
        }
        serialized_payload = json.dumps(payload_dict).encode("utf-8")
        
        # 2. Encrypt payload using authenticated AES-256-GCM
        ciphertext_blob = CryptoService.encrypt_payload(serialized_payload, passphrase)
        payload_sha256 = CryptoService.compute_sha256(ciphertext_blob)
        
        # 3. Split ciphertext into chunks with versioned 32-byte binary SEC1 headers
        chunk_frames = PayloadManager.split_payload(ciphertext_blob, num_images, msg_uuid)
        
        # 4. Save and embed each chunk into its corresponding cover image
        saved_stego_records = []
        temp_dir = current_app.config["TEMP_FOLDER"]
        stego_dir = current_app.config["STEGO_FOLDER"]
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(stego_dir, exist_ok=True)
        
        try:
            for idx, (f, frame) in enumerate(zip(cover_files, chunk_frames)):
                orig_name = secure_filename(f.filename)
                temp_cover = os.path.join(temp_dir, f"temp_{uuid.uuid4().hex}_{orig_name}")
                f.save(temp_cover)
                
                # Validate format & capacity
                val = ImageValidator.validate_image_file(temp_cover)
                stego_filename = f"stego_{msg_uuid[:8]}_chunk_{idx+1}_of_{num_images}.png"
                stego_dest = os.path.join(stego_dir, stego_filename)
                
                # Embed frame
                metrics = StegoEncoder.embed_frame_into_image(temp_cover, stego_dest, frame)
                
                # Clean up temporary cover upload
                if os.path.exists(temp_cover):
                    os.remove(temp_cover)
                    
                stego_rec = StegoImage(
                    chunk_index=idx,
                    total_chunks=num_images,
                    filename=stego_filename,
                    filepath=stego_dest,
                    original_filename=orig_name,
                    image_width=metrics["width"],
                    image_height=metrics["height"],
                    bytes_capacity=metrics["bytes_capacity"],
                    bytes_embedded=metrics["bytes_embedded"],
                    chunk_sha256=CryptoService.compute_sha256(frame)
                )
                saved_stego_records.append(stego_rec)
                
        except Exception as e:
            flash(f"Error during steganography encoding: {str(e)}", "danger")
            return render_template("communication/create_message.html", users=users)
            
        # 5. Persist message metadata in database (zero plaintext stored!)
        msg_record = Message(
            message_uuid=msg_uuid,
            sender_id=current_user.id,
            recipient_id=int(recipient_id) if recipient_id else None,
            title=title,
            requires_face_auth=require_face,
            total_chunks=num_images,
            payload_sha256=payload_sha256
        )
        db.session.add(msg_record)
        db.session.flush()
        
        for sr in saved_stego_records:
            sr.message_id = msg_record.id
            db.session.add(sr)
            
        db.session.commit()
        AuditLogService.log_event("STEGO_MESSAGE_ENCODED", user_id=current_user.id, details=f"UUID {msg_uuid} into {num_images} images")
        
        flash("Secret communication package successfully created and embedded!", "success")
        return redirect(url_for("communication.package_details", uuid=msg_uuid))
        
    return render_template("communication/create_message.html", users=users)

@comm_bp.route("/messages/package/<uuid>")
@login_required
def package_details(uuid):
    msg = Message.query.filter_by(message_uuid=uuid).first_or_404()
    # Authorization: sender or recipient
    if msg.sender_id != current_user.id and msg.recipient_id != current_user.id and not current_user.is_admin:
        abort(403)
    return render_template("communication/package_details.html", message=msg)

@comm_bp.route("/messages/download-chunk/<int:chunk_id>")
@login_required
def download_chunk(chunk_id):
    stego = StegoImage.query.get_or_404(chunk_id)
    msg = stego.message
    if msg.sender_id != current_user.id and msg.recipient_id != current_user.id and not current_user.is_admin:
        abort(403)
    return send_file(stego.filepath, as_attachment=True, download_name=stego.filename)

@comm_bp.route("/messages/download-all/<uuid>")
@login_required
def download_all_zip(uuid):
    msg = Message.query.filter_by(message_uuid=uuid).first_or_404()
    if msg.sender_id != current_user.id and msg.recipient_id != current_user.id and not current_user.is_admin:
        abort(403)
        
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for s in msg.stego_images:
            if os.path.exists(s.filepath):
                zf.write(s.filepath, arcname=s.filename)
    memory_file.seek(0)
    
    return send_file(
        memory_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"stego_package_{uuid[:8]}.zip"
    )

@comm_bp.route("/messages/extract", methods=["GET", "POST"])
@login_required
def extract_message():
    if request.method == "POST":
        passphrase = request.form.get("passphrase", "").strip()
        stego_files = request.files.getlist("stego_images")
        probe_face = request.files.get("probe_face_image")
        
        if not passphrase:
            flash("Passphrase is required to decrypt the extracted payload.", "danger")
            return render_template("steganography/extract.html")
            
        if not stego_files or len(stego_files) == 0 or stego_files[0].filename == "":
            flash("Please upload all stego images of the communication set.", "danger")
            return render_template("steganography/extract.html")
            
        temp_dir = current_app.config["TEMP_FOLDER"]
        os.makedirs(temp_dir, exist_ok=True)
        
        unpacked_chunks = []
        try:
            for f in stego_files:
                temp_stego = os.path.join(temp_dir, f"ext_{uuid.uuid4().hex}_{secure_filename(f.filename)}")
                f.save(temp_stego)
                
                # Extract chunk
                chunk_dict = StegoDecoder.extract_frame_from_image(temp_stego)
                unpacked_chunks.append(chunk_dict)
                
                if os.path.exists(temp_stego):
                    os.remove(temp_stego)
                    
            # Reconstruct the entire ciphertext blob
            reconstructed_ciphertext = PayloadManager.reconstruct_payload(unpacked_chunks)
            
        except Exception as e:
            flash(f"Extraction failed: {str(e)}", "danger")
            return render_template("steganography/extract.html")
            
        # Decrypt payload using authenticated AES-GCM
        try:
            decrypted_json_bytes = CryptoService.decrypt_payload(reconstructed_ciphertext, passphrase)
            secret_data = json.loads(decrypted_json_bytes.decode("utf-8"))
        except Exception as e:
            AuditLogService.log_event("STEGO_DECRYPTION_FAILED", user_id=current_user.id, status="FAILURE", details=str(e))
            flash(f"Decryption failed: {str(e)}", "danger")
            return render_template("steganography/extract.html")
            
        # Check if corresponding message in DB requires Face Verification
        msg_uuid = secret_data.get("uuid")
        db_msg = Message.query.filter_by(message_uuid=msg_uuid).first()
        
        if db_msg and db_msg.requires_face_auth:
            # Check recipient face verification
            if not current_user.face_profile:
                flash("This message requires facial identity verification, but you have no enrolled face profile. Please enroll in your profile.", "warning")
                return render_template("steganography/extract.html")
                
            if not probe_face or probe_face.filename == "":
                flash("This message requires live facial verification. Please upload or capture your face probe image.", "warning")
                return render_template("steganography/extract.html")
                
            probe_bytes = probe_face.read()
            enrolled_emb = current_user.face_profile.get_embedding()
            ver_res = FaceVerificationService.verify_probe(probe_bytes, enrolled_emb)
            
            if not ver_res["verified"]:
                AuditLogService.log_event("FACE_VERIFICATION_REJECTED", user_id=current_user.id, status="DENIED", details=f"Similarity: {ver_res.get('similarity_score')}")
                flash(f"Biometric face verification failed: {ver_res.get('message')} (Score: {ver_res.get('similarity_score')})", "danger")
                return render_template("steganography/extract.html")
                
            AuditLogService.log_event("FACE_VERIFICATION_PASSED", user_id=current_user.id, details=f"Score: {ver_res.get('similarity_score')}")
            
        # Update delivery status
        if db_msg:
            db_msg.is_delivered = True
            db_msg.is_extracted = True
            db_msg.extraction_count += 1
            db_msg.extracted_at = datetime.utcnow()
            db.session.commit()
            
        AuditLogService.log_event("STEGO_MESSAGE_DECRYPTED", user_id=current_user.id, details=f"UUID {msg_uuid}")
        
        # Display decrypted message in memory (never written plaintext to disk)
        return render_template("steganography/decrypted_view.html", secret_data=secret_data, total_chunks=len(unpacked_chunks))
        
    return render_template("steganography/extract.html")

@comm_bp.route("/messages/history")
@login_required
def history():
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    received = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.created_at.desc()).all()
    return render_template("communication/history.html", sent_messages=sent, received_messages=received)
