from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
        
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
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email already exists'}), 409

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful'}), 201