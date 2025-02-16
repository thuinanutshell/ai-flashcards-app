from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/status')
@cross_origin(supports_credentials=True) # what exactly does this do?
def auth_status():
    # Check Authorization header first
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.replace('Bearer ', '')
        try:
            user = User.query.get(int(token))
            if user:
                return jsonify({
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'name': user.name
                    }
                }), 200
        except:
            pass

    # Fall back to session-based auth
    if current_user.is_authenticated:
        return jsonify({
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'name': current_user.name
            }
        }), 200

    return jsonify({'error': 'Not authenticated'}), 401

@auth.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()
        
        if not user or not user.is_active or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        login_user(user, remember=True)
        token = str(user.id)  # Simple token generation

        return jsonify({
            'message': 'Logged in successfully',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/signup', methods=['POST'])
@cross_origin(supports_credentials=True)
def signup_post():
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
        password=generate_password_hash(password, method='pbkdf2:sha256'),
        is_active=True  # Ensure new users are active
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

    return jsonify({'message': 'Registration successful'}), 201

@auth.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
@login_required
def logout_post():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
