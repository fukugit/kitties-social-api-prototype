from flask import Flask
from api.routes import main_bp
from api.top import top_bp
from api.auth import auth_bp
from flask_jwt_extended import JWTManager


def create_app():
    api = Flask(__name__)
    api.config['JWT_SECRET_KEY'] = 'your_secret_key'  # 秘密鍵を設定してください
    jwt = JWTManager(api)

    # Blueprint
    api.register_blueprint(main_bp)
    api.register_blueprint(top_bp)
    api.register_blueprint(auth_bp)

    return api