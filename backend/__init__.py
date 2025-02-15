from datetime import timedelta
from flask import Flask, jsonify, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user
from os import environ
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "expose_headers": ["Set-Cookie"]
        }
    })

    # 🔒 Security & Config
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'fallback_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Update session configuration
    app.config.update(
        SESSION_COOKIE_SECURE=False,  # Set to True in production
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_NAME='flashcard_session',
        PERMANENT_SESSION_LIFETIME=timedelta(days=1)
    )

    # Ensure sessions are permanent by default
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # 🔄 Initialize database
    db.init_app(app)

    # Update login manager configuration
    login_manager.init_app(app)
    login_manager.login_view = None  # Disable redirect
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    @app.before_request
    def load_user_from_header():
        if not current_user.is_authenticated:
            auth_header = request.headers.get('Authorization')
            if (auth_header and auth_header.startswith('Bearer ')):
                token = auth_header.replace('Bearer ', '')
                try:
                    from .models import User
                    user = User.query.get(int(token))
                    if user:
                        login_user(user)
                except:
                    pass

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "Unauthorized"}), 401

    with app.app_context():
        try:
            from . import models  # Lazy import for faster app startup
            db.create_all()
            logger.info("✅ Database tables initialized successfully.")
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")

    # 🛠️ Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .folders import folders as folders_blueprint
    app.register_blueprint(folders_blueprint, url_prefix='/folders')

    from .cards import cards as cards_blueprint
    app.register_blueprint(cards_blueprint, url_prefix='/cards')
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    logger.info(f"🚀 Flask App Started - Mode: {environ.get('FLASK_ENV', 'development')}")
    return app
