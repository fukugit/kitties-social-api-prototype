from flask import Flask, jsonify
from flask import Blueprint

top_bp = Blueprint('top', __name__)

@top_bp.route('/top')
def hello():
    top = {
        'greeting': "Hello World!1"
    }
    return jsonify(top)
