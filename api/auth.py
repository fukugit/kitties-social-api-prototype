from flask import jsonify, request
from flask import Blueprint
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta, timezone

from utils.response import create_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if data is None:
        return create_response(message="Invalid JSON", code=-1, http_status=400)

    id = data.get("id")
    pw = data.get("pw")

    if id == "test" and pw == "test":
        # In order to use '@jwt_required()' of 'Authorization: Bearer', create JWR token.
        access_token = create_access_token(identity=id)
        return create_response({
            "access_token": access_token
        })
    else:
        return create_response(message="login error", code=-1)