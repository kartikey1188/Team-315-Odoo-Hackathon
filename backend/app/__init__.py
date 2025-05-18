from flask import Flask
from app.models import db, bcrypt
from flask_cors import CORS
from app.config import Config

def create_app(test_config=None):
    app = Flask(__name__, static_folder='../docs', static_url_path='/static')
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins=["http://localhost:5173", "https://deployment.com"], supports_credentials=True) 

    return app