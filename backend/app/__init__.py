from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "..", "finance_insights.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import file_routes, analysis_routes, dashboard_routes
    app.register_blueprint(file_routes.bp)
    app.register_blueprint(analysis_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    
    # Import models and create tables (must be after model imports)
    from app.models import Payment, Customer, FileUpload
    with app.app_context():
        db.create_all()
    
    return app
