from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'}), 400
        
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
        
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
        
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Log in user and create session
    login_user(user)
    
    return jsonify({
        'message': 'Logged in successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    }), 200

@auth.route('/signup', methods=['POST'])
def signup_post():
    if current_user.is_authenticated:
        return jsonify({'error': 'Already logged in'}), 400
        
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
        
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    
    if not email or not name or not password:
        return jsonify({'error': 'Email, name, and password are required'}), 400
    
    # Validate email format
    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400
        
    # Validate password strength
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email already exists'}), 409

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256')
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

    return jsonify({'message': 'Registration successful'}), 201

@auth.route('/logout', methods=['POST'])
def logout_post():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not logged in'}), 401
        
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200