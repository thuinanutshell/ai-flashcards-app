from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Folder, Card
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "API is running"}), 200

@main.route('/dashboard', methods=['GET'])
@login_required
def show_dashboard():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify({
        'user_id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'message': 'Successfully accessed dashboard'
    }), 200

@main.route('/folder', methods=['POST', 'PUT', 'DELETE', 'GET'])
@login_required
def folder_operations():
    if request.method=='POST':
        data = request.get_json()
        folder_name = data.get('folder_name')
        new_folder = Folder(folder_name=folder_name, user_id=current_user.id)
        db.session.add(new_folder)
        db.session.commit()
        return jsonify({
            'message': 'Successfully added a new folder',
            'folder_id': new_folder.id
            }), 201

    elif request.method=='DELETE':
        data = request.get_json()
        folder_name = data.get('folder_name')
        folder = Folder.query.filter_by(folder_name=folder_name).first()
        db.session.delete(folder)
        db.session.commit()
        if folder.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        return jsonify({'message': 'Successfully deleted a folder'}), 200

    elif request.method=='PUT':
        data = request.get_json()
        folder_name = data.get('folder_name')
        new_name = data.get('new_name')
        folder = Folder.query.filter_by(folder_name=folder_name).first()
        folder.folder_name = new_name
        db.session.commit()
        return jsonify({'message': 'Successfully edited the folder'}), 200

    

@main.route('/card', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def card_operations():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        folder_id = data.get('folder_id')
        card_question = data.get('card_question')
        card_answer = data.get('card_answer')
        
        if not all([folder_id, card_question, card_answer]):
            return jsonify({"error": "Missing required fields"}), 400
            
        # Verify folder exists and user has access
        folder = Folder.query.get(folder_id)
        if not folder or folder.user_id != current_user.id:
            return jsonify({"error": "Invalid folder or unauthorized access"}), 403
        
        new_card = Card(card_question=card_question, card_answer=card_answer, folder_id=folder_id)
        try:
            db.session.add(new_card)
            db.session.commit()
            return jsonify({
                'message': 'Added a new card!',
                'card_id': new_card.id,
                'card_question': new_card.card_question
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to create card"}), 500
        
    elif request.method == 'DELETE':
        data = request.get_json()
        if not data or 'id' not in data:
            return jsonify({"error": "Card ID is required"}), 400
            
        card_id = data.get('id')
        card = Card.query.get(card_id)
        
        if not card:
            return jsonify({"error": "Card not found"}), 404
            
        if card.folder.user_id != current_user.id:
            return jsonify({"error": "Unauthorized access"}), 403
            
        try:
            db.session.delete(card)
            db.session.commit()
            return jsonify({'message': 'Deleted card successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to delete card"}), 500
            
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        card_id = data.get('id')
        card_question = data.get('card_question')
        card_answer = data.get('card_answer')
        
        if not all([card_id, card_question, card_answer]):
            return jsonify({"error": "Missing required fields"}), 400
            
        card = Card.query.get(card_id)
        if not card:
            return jsonify({"error": "Card not found"}), 404
            
        if card.folder.user_id != current_user.id:
            return jsonify({"error": "Unauthorized access"}), 403
            
        try:
            card.card_question = card_question
            card.card_answer = card_answer
            db.session.commit()
            return jsonify({'message': 'Updated card successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to update card"}), 500
    
    elif request.method == 'GET':
        folder_name = request.args.get('folder_name')
        card_id = request.args.get('card_id')
        
        # If card_id is provided, return a single card
        if card_id:
            card = Card.query.get(card_id)
            
            if not card:
                return jsonify({"error": "Card not found"}), 404
                
            # Verify card ownership through folder relationship
            if card.folder.user_id != current_user.id:
                return jsonify({"error": "Unauthorized access to card"}), 403
                
            return jsonify({
                "id": card.id,
                "question": card.card_question,
                "answer": card.card_answer,
                "first_reviewed": card.first_reviewed,
                "second_reviewed": card.second_reviewed,
                "last_reviewed": card.last_reviewed,
                "created_at": card.created_at.isoformat(),
                "updated_at": card.updated_at.isoformat(),
                "last_reviewed_at": card.last_reviewed_at.isoformat() if card.last_reviewed_at else None,
                "folder_id": card.folder_id
            }), 200
        
        # If folder_name is provided, return all cards in the folder
        elif folder_name:
            folder = Folder.query.filter_by(folder_name=folder_name, user_id=current_user.id).first()
            
            if not folder:
                return jsonify({"error": "Folder not found or unauthorized"}), 404
            
            cards = Card.query.filter_by(folder_id=folder.id).all()
            
            cards_data = [{
                "id": card.id,
                "question": card.card_question,
                "answer": card.card_answer,
                "first_reviewed": card.first_reviewed,
                "second_reviewed": card.second_reviewed,
                "last_reviewed": card.last_reviewed,
                "created_at": card.created_at.isoformat(),
                "updated_at": card.updated_at.isoformat(),
                "last_reviewed_at": card.last_reviewed_at.isoformat() if card.last_reviewed_at else None
            } for card in cards]
            
            return jsonify({
                "folder_name": folder.folder_name,
                "folder_id": folder.id,
                "cards": cards_data,
                "total_cards": len(cards_data)
            }), 200
        
        else:
            return jsonify({"error": "Either folder_name or card_id is required"})
