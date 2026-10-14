from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, login_manager
from app.models.user import User
from app.models.face_profile import FaceProfile
from app.auth.forms import RegistrationForm, LoginForm, ChangePasswordForm, FaceEnrollmentForm
from app.security.permissions import AuditLogService
from app.face_recognition.enrollment import FaceEnrollmentService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("communication.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        AuditLogService.log_event("USER_REGISTRATION", user_id=user.id, details=f"Registered user {user.username} role {user.role}")
        flash("Registration successful! You may now log in to your account.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("communication.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.username.data.strip()
        user = User.query.filter((User.username == identifier) | (User.email == identifier.lower())).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash("Your account has been deactivated. Please contact an administrator.", "danger")
                AuditLogService.log_event("LOGIN_INACTIVE_ATTEMPT", user_id=user.id, status="FAILURE")
                return render_template("auth/login.html", form=form)
                
            login_user(user, remember=form.remember.data)
            session.permanent = True
            AuditLogService.log_event("USER_LOGIN_SUCCESS", user_id=user.id)
            flash(f"Welcome back, {user.username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("communication.dashboard"))
        else:
            AuditLogService.log_event("USER_LOGIN_FAILED", status="FAILURE", details=f"Failed attempt for {identifier}")
            flash("Invalid credentials. Please verify your username and password.", "danger")
            
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    uid = current_user.id
    logout_user()
    session.clear()
    AuditLogService.log_event("USER_LOGOUT", user_id=uid)
    flash("You have been securely logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile/profile.html", user=current_user)

@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            AuditLogService.log_event("PASSWORD_CHANGE_SUCCESS", user_id=current_user.id)
            flash("Your password has been updated successfully.", "success")
            return redirect(url_for("auth.profile"))
        else:
            flash("Current password incorrect.", "danger")
    return render_template("profile/change_password.html", form=form)

@auth_bp.route("/enroll-face", methods=["GET", "POST"])
@login_required
def enroll_face():
    form = FaceEnrollmentForm()
    if form.validate_on_submit():
        file = form.face_image.data
        image_bytes = file.read()
        consent_stmt = "Explicit user biometric enrollment consent provided via form submission."
        
        result = FaceEnrollmentService.enroll_face(image_bytes, consent_stmt)
        if result["success"]:
            # Delete existing face profile if present
            if current_user.face_profile:
                db.session.delete(current_user.face_profile)
                db.session.commit()
                
            fp = FaceProfile(
                user_id=current_user.id,
                has_consent=True,
                consent_statement=consent_stmt,
                algorithm_version=result["algorithm"]
            )
            fp.set_embedding(result["embedding"])
            db.session.add(fp)
            db.session.commit()
            
            AuditLogService.log_event("FACE_ENROLLMENT_SUCCESS", user_id=current_user.id)
            flash("Biometric face profile successfully enrolled for secondary verification!", "success")
            return redirect(url_for("auth.profile"))
        else:
            AuditLogService.log_event("FACE_ENROLLMENT_FAILED", user_id=current_user.id, status="FAILURE", details=result.get("error"))
            flash(f"Face enrollment failed: {result.get('error')}", "danger")
            
    return render_template("face_verification/enroll.html", form=form)

@auth_bp.route("/delete-face-profile", methods=["POST"])
@login_required
def delete_face_profile():
    if current_user.face_profile:
        db.session.delete(current_user.face_profile)
        db.session.commit()
        AuditLogService.log_event("FACE_PROFILE_DELETED", user_id=current_user.id)
        flash("Your biometric face profile has been permanently removed.", "info")
    return redirect(url_for("auth.profile"))
