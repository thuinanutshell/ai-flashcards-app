from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({
        "message": "AI Flashcards API",
        "status": "running",
        "version": "1.0"
    }), 200