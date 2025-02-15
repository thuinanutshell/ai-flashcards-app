from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from .models import Folder
from . import db

folders = Blueprint('folders', __name__)

@folders.route('/', methods=['GET'])
@login_required
@cross_origin(supports_credentials=True)
def get_folders():
    user_folders = Folder.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': folder.id,
        'name': folder.folder_name
    } for folder in user_folders]), 200

@folders.route('/create_folder', methods=['POST'])
@login_required
@cross_origin(supports_credentials=True)
def create_folder():
    # Remove session check since we're using flask_login
    data = request.get_json()
    folder_name = data.get('folder_name')

    if not folder_name:
        return jsonify({'error': 'Folder name is required'}), 400

    existing_folder = Folder.query.filter_by(
        folder_name=folder_name, 
        user_id=current_user.id
    ).first()
    
    if existing_folder:
        return jsonify({'error': 'Folder name already exists'}), 409

    new_folder = Folder(folder_name=folder_name, user_id=current_user.id)
    db.session.add(new_folder)
    db.session.commit()

    return jsonify({
        'message': 'Successfully added a new folder',
        'folder_id': new_folder.id,
        'folder_name': new_folder.folder_name,
    }), 201


@folders.route('/update_folder', methods=['PUT'])
@login_required
@cross_origin(supports_credentials=True)
def update_folder():
    data = request.get_json()
    folder_name = data.get('folder_name')
    new_name = data.get('new_name')

    folder = Folder.query.filter_by(folder_name=folder_name, user_id=current_user.id).first()

    if not folder:
        return jsonify({'error': 'Folder not found or unauthorized'}), 404
    
    folder.folder_name = new_name
    db.session.commit()

    return jsonify({'message': 'Successfully edited the folder'}), 200

@folders.route('/delete_folder', methods=['DELETE'])
@login_required
@cross_origin(supports_credentials=True)
def delete_folder():
    data = request.get_json()
    folder_name = data.get('folder_name')

    folder = Folder.query.filter_by(folder_name=folder_name, user_id=current_user.id).first()

    if not folder:
        return jsonify({'error': 'Folder not found or unauthorized'}), 404

    db.session.delete(folder)
    db.session.commit()
    
    return jsonify({'message': 'Successfully deleted the folder'}), 200