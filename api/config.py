import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

config = {
    'local': 'api.local_config.LocalConfig'
}

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    env_flask_config_name = os.getenv('MODE', 'local')
    app_config = config[env_flask_config_name]
    app.config.from_object(app_config)
    db.init_app(app)
    return app

app = create_app()