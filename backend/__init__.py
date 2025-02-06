from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

db = SQLAlchemy() # create a db object

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {"origins": "http://localhost:3000"}
    })
    
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)
    
    with app.app_context():
        from . import models  # Import models
        db.create_all()      # Create tables
    
    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # blueprint for non-auth routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
