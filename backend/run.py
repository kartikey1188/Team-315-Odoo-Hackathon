from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from app import create_app, db

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

if __name__ == '__main__':
    with app.app_context():
        from app.models import models
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "false").strip().lower() == "true"
    app.run(host='0.0.0.0', debug=debug_mode, port=port)