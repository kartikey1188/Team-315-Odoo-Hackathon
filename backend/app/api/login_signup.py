from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import bcrypt

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///users.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(80), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    
    if not all(k in data for k in ['email', 'password', 'name']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
    new_user = User(
        email=data['email'],
        password=hashed_password,
        name=data['name']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401