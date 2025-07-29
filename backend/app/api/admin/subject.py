from flask import request
from flask_restful import Resource, abort
from app.models import Subject
from app.extensions import db
from app.decorators.auth_decorators import admin_required
from app.utils.cache_utils import cache_response, rate_limit, invalidate_cache_for_subjects

class SubjectListResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self):
        try:
            subjects = Subject.query.all()
            result = []
            for subject in subjects:
                result.append({
                    'id': subject.id,
                    'name': subject.name,
                    'level': subject.level,
                    'description': subject.description,
                    'chapters': [
                        {
                            'id': chapter.id,
                            'name': chapter.name,
                            'description': chapter.description
                        }
                        for chapter in subject.chapters
                    ]
                })
            return result, 200
        except Exception as e:
            return {"msg": f"Failed to retrieve subjects: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def post(self):
        try:
            data = request.get_json()
            name = data.get('name')
            level = data.get('level')
            description = data.get('description')

            if not name:
                return {"msg": "Subject name is required"}, 400

            subject = Subject(name=name, level=level, description=description)
            db.session.add(subject)
            db.session.commit()
            invalidate_cache_for_subjects()

            return {"msg": "Subject created", "id": subject.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error creating subject: {str(e)}"}, 500

class SubjectResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self, subject_id):
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                abort(404, message="Subject not found")
            result = {
                'id': subject.id,
                'name': subject.name,
                'level': subject.level,
                'description': subject.description,
                'chapters': [
                    {
                        'id': chapter.id,
                        'name': chapter.name,
                        'description': chapter.description
                    }
                    for chapter in subject.chapters
                ]
            }

            return result, 200
        
        except Exception as e:
            return {"msg": f"Failed to retrieve subject: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def put(self, subject_id):
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                abort(404, message="Subject not found")

            data = request.get_json()
            subject.name = data.get('name', subject.name)
            subject.level = data.get('level', subject.level)
            subject.description = data.get('description', subject.description)

            db.session.commit()
            invalidate_cache_for_subjects()
            return {"msg": "Subject updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating subject: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def delete(self, subject_id):
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                abort(404, message="Subject not found")

            db.session.delete(subject)
            db.session.commit()
            invalidate_cache_for_subjects()
            return {"msg": "Subject deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error deleting subject: {str(e)}"}, 500
