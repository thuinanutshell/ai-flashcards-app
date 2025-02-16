from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from .models import Card, Folder
from . import db

cards = Blueprint('cards', __name__)

@cards.route('/get_cards', methods=['GET'])
@login_required
@cross_origin(supports_credentials=True)
def get_cards():
    folder_id = request.args.get('folder_id')
    card_id = request.args.get('card_id')

    if card_id:
        # Get a specific card
        card = Card.query.join(Folder).filter(
            Card.id == card_id,
            Folder.user_id == current_user.id
        ).first()
        
        if not card:
            return jsonify({'error': 'Card not found or unauthorized'}), 404
            
        return jsonify({
            'id': card.id,
            'question': card.card_question,
            'answer': card.card_answer,
            'folder_id': card.folder_id,
            'first_reviewed': card.first_reviewed,
            'second_reviewed': card.second_reviewed,
            'last_reviewed': card.last_reviewed,
            'last_reviewed_at': card.last_reviewed_at
        }), 200

    elif folder_id:
        # Get all cards in a folder by folder_id
        folder = Folder.query.filter_by(
            id=folder_id,
            user_id=current_user.id
        ).first()
        
        if not folder:
            return jsonify({'error': 'Folder not found or unauthorized'}), 404
            
        cards = Card.query.filter_by(folder_id=folder.id).all()
        return jsonify([{
            'id': card.id,
            'question': card.card_question,
            'answer': card.card_answer,
            'first_reviewed': card.first_reviewed,
            'second_reviewed': card.second_reviewed,
            'last_reviewed': card.last_reviewed,
            'last_reviewed_at': card.last_reviewed_at
        } for card in cards]), 200
    
    # If no parameters provided, return all cards for the user
    cards = Card.query.join(Folder).filter(
        Folder.user_id == current_user.id
    ).all()
    
    return jsonify([{
        'id': card.id,
        'question': card.card_question,
        'answer': card.card_answer,
        'folder_id': card.folder_id,
        'first_reviewed': card.first_reviewed,
        'second_reviewed': card.second_reviewed,
        'last_reviewed': card.last_reviewed,
        'last_reviewed_at': card.last_reviewed_at
    } for card in cards]), 200


@cards.route('/create_card', methods=['POST'])
@login_required
@cross_origin(supports_credentials=True)
def create_card():
    data = request.get_json()
    
    # Validate required fields
    if not all(field in data for field in ['folder_name', 'question', 'answer']):
        return jsonify({
            'error': 'Missing required fields. Please provide folder_name, question, and answer'
        }), 400

    # Get the folder
    folder = Folder.query.filter_by(
        folder_name=data['folder_name'],
        user_id=current_user.id
    ).first()

    if not folder:
        return jsonify({'error': 'Folder not found'}), 404

    # Create new card
    new_card = Card(
        card_question=data['question'],
        card_answer=data['answer'],
        folder_id=folder.id
    )

    db.session.add(new_card)
    db.session.commit()

    return jsonify({
        'message': 'Card created successfully',
        'card': {
            'id': new_card.id,
            'question': new_card.card_question,
            'answer': new_card.card_answer,
            'folder_id': new_card.folder_id
        }
    }), 201


@cards.route('/update_card', methods=['PUT'])
@login_required
@cross_origin(supports_credentials=True)
def update_card():
    data = request.get_json()
    
    # Validate required fields
    if not all(field in data for field in ['card_id', 'question', 'answer']):
        return jsonify({
            'error': 'Missing required fields. Please provide card_id, question, and answer'
        }), 400

    # Get the card and verify ownership
    card = Card.query.join(Folder).filter(
        Card.id == data['card_id'],
        Folder.user_id == current_user.id
    ).first()

    if not card:
        return jsonify({'error': 'Card not found or unauthorized'}), 404

    # Update card fields
    card.card_question = data['question']
    card.card_answer = data['answer']
    
    # Update review status if provided
    if 'first_reviewed' in data:
        card.first_reviewed = data['first_reviewed']
    if 'second_reviewed' in data:
        card.second_reviewed = data['second_reviewed']
    if 'last_reviewed' in data:
        card.last_reviewed = data['last_reviewed']
        card.last_reviewed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'message': 'Card updated successfully',
        'card': {
            'id': card.id,
            'question': card.card_question,
            'answer': card.card_answer,
            'first_reviewed': card.first_reviewed,
            'second_reviewed': card.second_reviewed,
            'last_reviewed': card.last_reviewed,
            'last_reviewed_at': card.last_reviewed_at
        }
    }), 200


@cards.route('/delete_card', methods=['DELETE'])
@login_required
@cross_origin(supports_credentials=True)
def delete_card():
    data = request.get_json()
    
    if 'card_id' not in data:
        return jsonify({
            'error': 'Missing required field: card_id'
        }), 400

    # Get the card and verify ownership
    card = Card.query.join(Folder).filter(
        Card.id == data['card_id'],
        Folder.user_id == current_user.id
    ).first()

    if not card:
        return jsonify({'error': 'Card not found or unauthorized'}), 404

    db.session.delete(card)
    db.session.commit()

    return jsonify({
        'message': 'Card deleted successfully',
        'card_id': data['card_id']
    }), 200
