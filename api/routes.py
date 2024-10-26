from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = {
        'greeting': "top!"
    }
    return jsonify(page)

@main_bp.route('/about')
def about():
    page = {
        'greeting': "about!"
    }
    return jsonify(page)