from flask import Blueprint, jsonify, Flask
from api import db
from api.model import Cat

cat_bp = Blueprint('cat', __name__)

# テストapiです
@cat_bp.route('/cat')
def get_all_cat():
    cats = db.session.query(Cat)
    cats_data = [
        {
            "id": cat.id,
            "name": cat.name,
            "breed": cat.breed,
            "created_at": cat.created_at
        } for cat in cats
    ]
    return jsonify(cats_data)
