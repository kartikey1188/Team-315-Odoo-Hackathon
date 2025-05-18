from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from . import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='assignee_user', foreign_keys='Task.assignee_id')
    projects = db.relationship('Project', backref='created_by_user', foreign_keys='Project.created_by')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    tasks = db.relationship('Task', backref='project', lazy=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='TODO')  # TODO, IN_PROGRESS, DONE
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)