from flask import jsonify, request, g  
from flask_restful import Resource, Api  
from datetime import datetime
from app.models.models import db, Project, Task, Team, User, team_members
from app import app
from app.api.notifications import notify_task_assignment, notify_team_addition, notify_task_status_change

api = Api(app)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'User already exists'}, 409
        
        try:
            new_user = User(
                email=data['email'],
                password=data['password'],
                name=data['name']
            )
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.password == data['password']:
            return {'message': 'Login successful'}, 200
        
        return {'message': 'Invalid credentials'}, 401

class ProjectResource(Resource):
    def get(self, project_id=None):
        if project_id:
            project = Project.query.get(project_id)
            if not project:
                return {'message': 'Project not found'}, 404
            
            return {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'created_at': project.created_at.isoformat(),
                'team_id': project.team_id
            }, 200
        else:
            projects = Project.query.all()
            result = []
            for project in projects:
                result.append({
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'created_at': project.created_at.isoformat(),
                    'team_id': project.team_id
                })
            return result, 200
    
    def post(self):
        data = request.get_json()
        
        try:
            new_project = Project(
                name=data['name'],
                description=data.get('description', ''),
                team_id=data['team_id']
            )
            db.session.add(new_project)
            db.session.commit()
            return {
                'id': new_project.id,
                'name': new_project.name,
                'description': new_project.description,
                'created_at': new_project.created_at.isoformat(),
                'team_id': new_project.team_id
            }, 201
        except Exception as e:
            return {'message': str(e)}, 500
    
    def put(self, project_id):
        project = Project.query.get(project_id)
        if not project:
            return {'message': 'Project not found'}, 404
        
        data = request.get_json()
        
        try:
            if 'name' in data:
                project.name = data['name']
            if 'description' in data:
                project.description = data['description']
            if 'team_id' in data:
                project.team_id = data['team_id']
            
            db.session.commit()
            return {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'created_at': project.created_at.isoformat(),
                'team_id': project.team_id
            }, 200
        except Exception as e:
            return {'message': str(e)}, 500
    
    def delete(self, project_id):
        project = Project.query.get(project_id)
        if not project:
            return {'message': 'Project not found'}, 404
        
        try:
            db.session.delete(project)
            db.session.commit()
            return {'message': 'Project deleted successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

class TeamResource(Resource):
    def get(self, team_id=None):
        if team_id:
            team = Team.query.get(team_id)
            if not team:
                return {'message': 'Team not found'}, 404
            
            members = [{'id': user.id, 'name': user.name, 'email': user.email} 
                      for user in team.members]
            
            return {
                'id': team.id,
                'name': team.name,
                'leader_id': team.leader_id,
                'members': members
            }, 200
        else:
            teams = Team.query.all()
            result = []
            for team in teams:
                result.append({
                    'id': team.id,
                    'name': team.name,
                    'leader_id': team.leader_id
                })
            return result, 200
    
    def post(self):
        data = request.get_json()
        
        try:
            new_team = Team(
                name=data['name'],
                leader_id=data['leader_id']
            )
            db.session.add(new_team)
            db.session.commit()
            
            leader = User.query.get(data['leader_id'])
            if leader:
                new_team.members.append(leader)
                db.session.commit()
            
            return {
                'id': new_team.id,
                'name': new_team.name,
                'leader_id': new_team.leader_id
            }, 201
        except Exception as e:
            return {'message': str(e)}, 500

class TeamMemberResource(Resource):
    def post(self, team_id):
        team = Team.query.get(team_id)
        if not team:
            return {'message': 'Team not found'}, 404
        
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return {'message': 'User ID is required'}, 400
        
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        if user in team.members:
            return {'message': 'User is already a member of this team'}, 400
        
        try:
            team.members.append(user)
            db.session.commit()
            
            # Sending notification email to the user
            notify_team_addition(user.email, team.name)
            
            return {'message': 'User added to team successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500
    
    def delete(self, team_id, user_id):
        team = Team.query.get(team_id)
        if not team:
            return {'message': 'Team not found'}, 404
        
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        if user not in team.members:
            return {'message': 'User is not a member of this team'}, 400
        
        if team.leader_id == user.id:
            return {'message': 'Cannot remove team leader from team'}, 400
        
        try:
            team.members.remove(user)
            db.session.commit()
            return {'message': 'User removed from team successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

class TaskResource(Resource):
    def get(self, project_id=None, task_id=None):
        if task_id:
            task = Task.query.get(task_id)
            if not task:
                return {'message': 'Task not found'}, 404
            
            return {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'created_at': task.created_at.isoformat(),
                'project_id': task.project_id,
                'assignee_id': task.assignee_id
            }, 200
        elif project_id:
            tasks = Task.query.filter_by(project_id=project_id).all()
            result = []
            for task in tasks:
                result.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'created_at': task.created_at.isoformat(),
                    'project_id': task.project_id,
                    'assignee_id': task.assignee_id
                })
            return result, 200
        else:
            return {'message': 'Project ID is required'}, 400
    
    def post(self, project_id):
        project = Project.query.get(project_id)
        if not project:
            return {'message': 'Project not found'}, 404
        
        data = request.get_json()
        
        try:
            due_date = None
            if 'due_date' in data and data['due_date']:
                due_date = datetime.fromisoformat(data['due_date'])
            
            new_task = Task(
                title=data['title'],
                description=data.get('description', ''),
                status=data.get('status', 'TO-DO'),
                due_date=due_date,
                project_id=project_id,
                assignee_id=data.get('assignee_id')
            )
            db.session.add(new_task)
            db.session.commit()
            
            # Sending notification email if task is assigned to someone
            if new_task.assignee_id:
                assignee = User.query.get(new_task.assignee_id)
                if assignee:
                    notify_task_assignment(assignee.email, new_task.title, project.name)
            
            return {
                'id': new_task.id,
                'title': new_task.title,
                'description': new_task.description,
                'status': new_task.status,
                'due_date': new_task.due_date.isoformat() if new_task.due_date else None,
                'created_at': new_task.created_at.isoformat(),
                'project_id': new_task.project_id,
                'assignee_id': new_task.assignee_id
            }, 201
        except Exception as e:
            return {'message': str(e)}, 500
    
    def put(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {'message': 'Task not found'}, 404
        
        data = request.get_json()
        old_status = task.status
        old_assignee_id = task.assignee_id
        
        try:
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'status' in data:
                task.status = data['status']
            if 'due_date' in data:
                task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
            if 'assignee_id' in data:
                task.assignee_id = data['assignee_id']
            
            db.session.commit()
            
            # Sending notification if the status has changed
            if old_status != task.status and task.assignee_id:
                assignee = User.query.get(task.assignee_id)
                if assignee:
                    notify_task_status_change(assignee.email, task.title, old_status, task.status)
            
            # Sending notification if the task has been reassigned
            if old_assignee_id != task.assignee_id and task.assignee_id:
                assignee = User.query.get(task.assignee_id)
                if assignee:
                    notify_task_assignment(assignee.email, task.title, task.project.name)
            
            return {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'created_at': task.created_at.isoformat(),
                'project_id': task.project_id,
                'assignee_id': task.assignee_id
            }, 200
        except Exception as e:
            return {'message': str(e)}, 500
    
    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {'message': 'Task not found'}, 404
        
        try:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

api.add_resource(UserRegistration, '/api/register')
api.add_resource(UserLogin, '/api/login')
api.add_resource(ProjectResource, '/api/projects', '/api/projects/<int:project_id>')
api.add_resource(TeamResource, '/api/teams', '/api/teams/<int:team_id>')
api.add_resource(TeamMemberResource, '/api/teams/<int:team_id>/members', '/api/teams/<int:team_id>/members/<int:user_id>')
api.add_resource(TaskResource, '/api/projects/<int:project_id>/tasks', '/api/tasks/<int:task_id>')


