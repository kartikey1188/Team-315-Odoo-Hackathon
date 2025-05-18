from flask import jsonify, request, g  
from flask_restful import Resource, Api  
from datetime import datetime
from models import db, Project, Task
from app import app

class ProjectListResource(Resource):
    def get(self):
        current_user = g.current_user  
        projects = Project.query.all()
        return jsonify([{
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
            'created_by': project.created_by
        } for project in projects])

    def post(self):
        current_user = g.current_user
        data = request.json
        new_project = Project(
            name=data['name'],
            description=data.get('description', ''),
            created_by=current_user.id
        )
        db.session.add(new_project)
        db.session.commit()
        return jsonify({
            'id': new_project.id,
            'name': new_project.name,
            'description': new_project.description,
            'created_at': new_project.created_at.isoformat(),
            'created_by': new_project.created_by
        }), 201

class ProjectResource(Resource):
    def get(self, project_id):
        current_user = g.current_user
        project = Project.query.get_or_404(project_id)
        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
            'created_by': project.created_by
        })

    def put(self, project_id):
        current_user = g.current_user
        project = Project.query.get_or_404(project_id)
        if project.created_by != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        data = request.json
        project.name = data.get('name', project.name)
        project.description = data.get('description', project.description)
        db.session.commit()
        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
            'created_by': project.created_by
        })

    def delete(self, project_id):
        current_user = g.current_user
        project = Project.query.get_or_404(project_id)
        if project.created_by != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        db.session.delete(project)
        db.session.commit()
        return '', 204

class TaskListResource(Resource):
    def get(self, project_id):
        current_user = g.current_user
        tasks = Task.query.filter_by(project_id=project_id).all()
        return jsonify([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'created_at': task.created_at.isoformat(),
            'assignee_id': task.assignee_id
        } for task in tasks])

    def post(self, project_id):
        current_user = g.current_user
        project = Project.query.get_or_404(project_id)
        data = request.json
        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'TODO'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            project_id=project_id,
            assignee_id=data.get('assignee_id')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            'id': new_task.id,
            'title': new_task.title,
            'description': new_task.description,
            'status': new_task.status,
            'due_date': new_task.due_date.isoformat() if new_task.due_date else None,
            'created_at': new_task.created_at.isoformat(),
            'assignee_id': new_task.assignee_id
        }), 201

class TaskResource(Resource):
    def put(self, task_id):
        current_user = g.current_user
        task = Task.query.get_or_404(task_id)
        project = Project.query.get(task.project_id)
        if project.created_by != current_user.id and task.assignee_id != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        data = request.json
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else task.due_date
        task.assignee_id = data.get('assignee_id', task.assignee_id)
        db.session.commit()
        return jsonify({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'created_at': task.created_at.isoformat(),
            'assignee_id': task.assignee_id
        })

    def delete(self, task_id):
        current_user = g.current_user
        task = Task.query.get_or_404(task_id)
        project = Project.query.get(task.project_id)
        if project.created_by != current_user.id:
            return jsonify({'message': 'Unauthorized'}), 403
        db.session.delete(task)
        db.session.commit()
        return '', 204

api = Api(app)
api.add_resource(ProjectListResource, '/api/projects')
api.add_resource(ProjectResource, '/api/projects/<int:project_id>')
api.add_resource(TaskListResource, '/api/projects/<int:project_id>/tasks')
api.add_resource(TaskResource, '/api/tasks/<int:task_id>')