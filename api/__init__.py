import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

config = {
    'local': 'env_config.LocalConfig'
}

db = SQLAlchemy()

def create_app():
    api = Flask(__name__)
    env_flask_config_name = os.getenv('MODE', 'local')
    app_config = config[env_flask_config_name]
    api.config.from_object(app_config)

    jwt = JWTManager(api)
    db.init_app(api)

    add_bluepoint(api)

    return api

def add_bluepoint(api):
    from api.cat import cat_bp
    from api.routes import main_bp
    from api.top import top_bp
    from api.auth import auth_bp
    # Blueprint
    api.register_blueprint(main_bp)
    api.register_blueprint(top_bp)
    api.register_blueprint(auth_bp)
    api.register_blueprint(cat_bp)