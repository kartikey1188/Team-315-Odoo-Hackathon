from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from app import create_app, db
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

load_dotenv()

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Swagger UI setup
SWAGGER_URL = ''  # Swagger UI served at localhost:5000
API_URL = '/static/openapi.yaml'  # the static folder is backend/docs folder

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Team 315 Odoo Hackathon"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    with app.app_context():
        from app.models import models
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "false").strip().lower() == "true"
    app.run(host='0.0.0.0', debug=debug_mode, port=port)