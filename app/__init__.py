import os
from flask import Flask, render_template
from config import config_by_name
from app.extensions import db, login_manager, csrf, migrate

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Ensure storage paths exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["STEGO_FOLDER"], exist_ok=True)
    os.makedirs(app.config["TEMP_FOLDER"], exist_ok=True)
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.communication.routes import comm_bp
    from app.deep_learning.routes import dl_bp
    from app.analytics.routes import analytics_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(comm_bp)
    app.register_blueprint(dl_bp)
    app.register_blueprint(analytics_bp)
    
    # Register error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403
        
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404
        
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500
        
    return app
