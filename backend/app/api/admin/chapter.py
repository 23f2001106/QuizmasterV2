from flask import request
from flask_restful import Resource,  abort
from app.models import Subject, Chapter
from app.extensions import db
from app.decorators.auth_decorators import admin_required
from app.utils.cache_utils import cache_response, invalidate_cache_for_chapters, rate_limit


class AllChaptersResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self):
        try:
            chapters = Chapter.query.all()
            chapters_data = [ 
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "subject_id": c.subject_id
                } for c in chapters
            ]
            return chapters_data, 200
        except Exception as e:
            return {"msg": f"Error retrieving chapters: {str(e)}"}, 500


class SubjectChapterListResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self, subject_id):
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                abort(404, message="Subject not found")

            chapters_data = [
                {
                    "id": c.id,
                    "name": c.name,
                    "description": c.description,
                    "subject_id": c.subject_id
                } for c in subject.chapters
            ]
            return chapters_data, 200
        except Exception as e:
            return {"msg": f"Error fetching chapters: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def post(self, subject_id):
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                abort(404, message="Subject not found")

            data = request.get_json()
            name = data.get('name')
            description = data.get('description')

            if not name:
                return {"msg": "Chapter name is required"}, 400

            chapter = Chapter(name=name, description=description, subject_id=subject.id)
            db.session.add(chapter)
            db.session.commit()

            invalidate_cache_for_chapters()

            return {"msg": "Chapter created", "id": chapter.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error creating chapter: {str(e)}"}, 500

class ChapterResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self, chapter_id):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                abort(404, message="Chapter not found")
            
            chapter_data = {
                "id": chapter.id,
                "name": chapter.name,
                "description": chapter.description,
                "subject_id": chapter.subject_id
            }
            return chapter_data, 200
        except Exception as e:
            return {"msg": f"Error retrieving chapter: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def put(self, chapter_id):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                abort(404, message="Chapter not found")

            data = request.get_json()
            chapter.name = data.get('name', chapter.name)
            chapter.description = data.get('description', chapter.description)

            db.session.commit()

            invalidate_cache_for_chapters()

            return {"msg": "Chapter updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating chapter: {str(e)}"}, 500

    @rate_limit(limit=100, window=60)
    def delete(self, chapter_id):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                abort(404, message="Chapter not found")

            db.session.delete(chapter)
            db.session.commit()

            invalidate_cache_for_chapters()
            
            return {"msg": "Chapter deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error deleting chapter: {str(e)}"}, 500
