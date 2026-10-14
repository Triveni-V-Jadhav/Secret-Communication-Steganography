from functools import wraps
from flask import abort, flash, redirect, url_for, request
from flask_login import current_user
from app.extensions import db
from app.models.audit_log import AuditLog

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        if not current_user.is_admin:
            AuditLogService.log_event(
                user_id=current_user.id,
                action="UNAUTHORIZED_ADMIN_ACCESS_ATTEMPT",
                status="DENIED",
                details=f"Attempted access to {request.path}"
            )
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

class AuditLogService:
    @staticmethod
    def log_event(action: str, user_id: int = None, status: str = "SUCCESS", details: str = None, ip_address: str = None):
        try:
            if ip_address is None and request:
                ip_address = request.remote_addr
        except Exception:
            ip_address = "127.0.0.1"
            
        entry = AuditLog(
            user_id=user_id,
            action=action,
            status=status,
            details=details[:500] if details else None,
            ip_address=ip_address
        )
        db.session.add(entry)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
