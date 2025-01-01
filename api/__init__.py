import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# 環境別用のconfig list
configurations = {
    'local': 'env_config.LocalConfig',
    'development': 'env_config.DevelopmentConfig'
}

db = SQLAlchemy()

def create_app():
    api = Flask(__name__)
    env_flask_config_name = os.getenv('MODE', 'local')
    app_config = configurations[env_flask_config_name]
    api.config.from_object(app_config)

    jwt = JWTManager(api)
    db.init_app(api)
    add_bluepoint(api)

    return api

def add_bluepoint(api):
    # import順序を変更するため
    from api.cat import cat_bp
    from api.routes import main_bp
    from api.top import top_bp
    from api.auth import auth_bp
    from api.file import file_bp
    from api.stripe import stripe_bp
    from api.payment_intent import payment_intent_bp
    # Blueprint
    api.register_blueprint(main_bp)
    api.register_blueprint(top_bp)
    api.register_blueprint(auth_bp)
    api.register_blueprint(cat_bp)
    api.register_blueprint(file_bp)
    api.register_blueprint(stripe_bp)
    api.register_blueprint(payment_intent_bp)