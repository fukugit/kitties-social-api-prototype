from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from api import db
from api.model import Cat
from utils.response import create_response

cat_bp = Blueprint('cat', __name__, url_prefix='/cat')

# テストapiです
# cat_informationにある全てのrecordを出してreturn
@cat_bp.route('/get_all', methods=['GET'])
def get_all_cat():
    cats = db.session.query(Cat).all()
    cats_data = [
        {
            'id': cat.id,
            'name': cat.name,
            'breed': cat.breed,
            'created_at': cat.created_at
        } for cat in cats
    ]
    return create_response(data={"cat_data": cats_data})

# cat_informationにone recordを追加
@cat_bp.route('/add', methods=['POST'])
def add_cat():
    cat = Cat(name='test_cat', breed='test_breed', nickname='')
    db.session.add(cat)
    db.session.flush()
    db.session.commit()
    return create_response(data={'id': cat.id})

# requestに設定したidのcat_informationのnameをrequestにあるnameに更新
@cat_bp.route('/update', methods=['POST'])
def change_name():
    data = request.json
    cat = db.session.query(Cat).get(data['id'])
    cat.name = data['name']
    db.session.commit()
    return create_response()

# jwt検証．identityが1以外であれば401
@cat_bp.route('/check_jwt', methods=['POST'])
@jwt_required()
def check_jwt():
    id = get_jwt_identity()
    if id == 1:
        return create_response()
    else:
        return create_response(message='invalid token', http_status=401)

# identity=1のjwtを作成
@cat_bp.route('/get_token', methods=['POST'])
def get_token():
    access_token = create_access_token(identity=1)
    return create_response(data={'access_token': access_token})
