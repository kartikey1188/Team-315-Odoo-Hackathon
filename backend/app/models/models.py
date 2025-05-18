from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from . import db, bcrypt

# Association table for team members
team_members = db.Table('team_members',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='assignee_user', foreign_keys='Task.assignee_id')
    teams_led = db.relationship('Team', backref='team_leader', lazy=True)
    member_of = db.relationship('Team', secondary=team_members, backref=db.backref('members', lazy='dynamic'))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    projects = db.relationship('Project', backref='team', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    tasks = db.relationship('Task', backref='project', lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='TO-DO')  # TO-DO, IN_PROGRESS, DONE
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))