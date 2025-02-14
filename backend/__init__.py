from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from os import environ
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

db = SQLAlchemy()  # create a db object
login_manager = LoginManager()  # create a login manager object

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
            }
    })
    
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    
    # Initialize the app's database
    db.init_app(app)
    
    # Configure Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login_post'  # Set the login view
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import here to avoid circular imports
        return User.query.get(int(user_id))
    
    with app.app_context():
        from . import models
        db.create_all()
        print("Database tables created successfully")
    
    # Register the blueprints of different features
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # Add URL prefix
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
