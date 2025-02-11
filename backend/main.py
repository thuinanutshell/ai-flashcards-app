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
    return "Profile"

@main.route('/folder', methods=['POST', 'PUT', 'DELETE'])
@login_required
def folder_operations():
    if request.method=='POST':
        data = request.get_json()
        folder_name = data.get('folder_name')
        new_folder = Folder(folder_name=folder_name, user_id=current_user.id)
        db.session.add(new_folder)
        db.session.commit()
        return jsonify({'message': 'Successfully added a new folder'}), 201

    elif request.method=='DELETE':
        data = request.get_json()
        folder_name = data.get('folder_name')
        folder = Folder.query.filter_by(folder_name=folder_name).first()
        db.session.delete(folder)
        db.session.commit()
        if folder.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        return jsonify({'message': 'Successfully deleted a folder'}), 200

    if request.method=='PUT':
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
        folder_id = data.get('folder_id')
        card_question = data.get('card_question')
        card_answer = data.get('card_answer')
        
        new_card = Card(card_question = card_question, card_answer = card_answer, folder_id=folder_id)
        db.session.add(new_card)
        db.session.commit()
        return jsonify({'message': 'Added a new card!'}), 201
        
    elif request.method == 'DELETE':
        data = request.get_json()
        card_id = data.get('id')
        card = Card.query.get(card_id)
        db.session.delete(card)
        db.session.commit()
        return jsonify({'message': 'Deleted a card successfully'}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        card_id = data.get('id')
        card_question = data.get('card_question')
        card_answer = data.get('card_answer')
        
        card = Card.query.get(card_id)
        if card:
            card.card_question = card_question
            card.card_answer = card_answer
        db.session.commit()
        return jsonify({'message': 'Saved a new updated card'}), 200
    
    elif request.method == 'GET':
        try:
            card_question = request.args.get('card_question')
            if not card_question:
                return jsonify({"error": "card_question is not required"}), 400
            
            card = Card.query.get_or_404(card_id)
            if not card:
                return jsonify({"error": "Card not found"}), 404
            
            return jsonify({
                "id": card.id,
                "question": card.card_question,
                "answer": card.card_answer
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
