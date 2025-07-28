from flask import request
from flask_restful import Resource, fields, marshal_with, abort
from app.models import Subject, Chapter
from app.extensions import db
from app.decorators.auth_decorators import admin_required


chapter_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'subject_id': fields.Integer
}

class AllChaptersResource(Resource):
    method_decorators = [admin_required]

    @marshal_with(chapter_fields)
    def get(self):
        try:
            chapters = Chapter.query.all()
            return chapters, 200
        except Exception as e:
            return {"msg": f"Error retrieving chapters: {str(e)}"}, 500


class SubjectChapterListResource(Resource):
    method_decorators = [admin_required]

    @marshal_with(chapter_fields)
    def get(self, subject_id):
        try:
            subject = Subject.query.get(subject_id)
            if not subject:
                abort(404, message="Subject not found")

            return subject.chapters, 200
        except Exception as e:
            return {"msg": f"Error fetching chapters: {str(e)}"}, 500

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

            return {"msg": "Chapter created", "id": chapter.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error creating chapter: {str(e)}"}, 500

class ChapterResource(Resource):
    method_decorators = [admin_required]

    @marshal_with(chapter_fields)
    def get(self, chapter_id):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                abort(404, message="Chapter not found")
            return chapter, 200
        except Exception as e:
            return {"msg": f"Error retrieving chapter: {str(e)}"}, 500

    def put(self, chapter_id):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                abort(404, message="Chapter not found")

            data = request.get_json()
            chapter.name = data.get('name', chapter.name)
            chapter.description = data.get('description', chapter.description)

            db.session.commit()
            return {"msg": "Chapter updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating chapter: {str(e)}"}, 500

    def delete(self, chapter_id):
        try:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                abort(404, message="Chapter not found")

            db.session.delete(chapter)
            db.session.commit()
            return {"msg": "Chapter deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error deleting chapter: {str(e)}"}, 500
