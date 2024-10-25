from flask import Flask, jsonify, request
from flask import Blueprint
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if data is None:
      return jsonify({"error": "Invalid JSON"}), 400

    id = data.get("id")
    pw = data.get("pw")

    if id == "test" and pw == "test":
        # In order to use '@jwt_required()' of 'Authorization: Bearer', create JWR token.
        access_token = create_access_token(identity=id)
        return jsonify({"result": "success", "access_token": access_token})
    else:
        return jsonify({"result": "error"})