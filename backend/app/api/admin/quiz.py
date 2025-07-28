from flask import request
from flask_restful import Resource, fields, marshal_with, abort
from app.models import Quiz
from app.extensions import db
from app.decorators.auth_decorators import admin_required
from datetime import datetime

# For question titles under a quiz
question_summary_fields = {
    'id': fields.Integer,
    'question_statement': fields.String
}

# For listing all quizzes
quiz_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_of_quiz': fields.DateTime(dt_format='iso8601'),
    'due_date': fields.DateTime(dt_format='iso8601'),
    'time_duration': fields.String,
    'remarks': fields.String,
    'date_created': fields.DateTime(dt_format='iso8601'),
    'questions': fields.List(fields.Nested(question_summary_fields)),
    'chapter': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'subject': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    })
}

class QuizListResource(Resource):
    method_decorators = [admin_required]

    @marshal_with(quiz_list_fields)
    def get(self):
        try:
            quizzes = Quiz.query.all()
            for quiz in quizzes:
                _ = quiz.chapter.subject
            return quizzes, 200
        except Exception as e:
            return {"msg": f"Error retrieving quizzes: {str(e)}"}, 500

    def post(self):
        try:
            data = request.get_json()
            name = data.get('name')
            chapter_id = data.get('chapter_id')
            date_of_quiz = datetime.fromisoformat(data.get('date_of_quiz'))
            due_date = datetime.fromisoformat(data.get('due_date'))
            time_duration = data.get('time_duration')  # "HH:MM:SS"

            if not all([name, chapter_id, date_of_quiz, due_date, time_duration]):
                return {"msg": "Missing required fields"}, 400

            quiz = Quiz(
                name=name,
                chapter_id=chapter_id,
                date_of_quiz=date_of_quiz,
                due_date=due_date,
                time_duration=datetime.strptime(time_duration, "%H:%M:%S").time(),
                remarks=data.get('remarks')
            )
            db.session.add(quiz)
            db.session.commit()

            return {"msg": "Quiz created", "id": quiz.id}, 201
        except Exception as e:
            db.session.rollback()
            print("msg:" f"Error creating quiz: {str(e)}")
            return {"msg": f"Error creating quiz: {str(e)}"}, 500

class QuizResource(Resource):
    method_decorators = [admin_required]

    def get(self, quiz_id):
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, message="Quiz not found")

            chapter = quiz.chapter
            subject = chapter.subject

            quiz_data = {
                'id': quiz.id,
                'name': quiz.name,
                'date_of_quiz': quiz.date_of_quiz.isoformat(),
                'due_date': quiz.due_date.isoformat(),
                'time_duration': str(quiz.time_duration),
                'remarks': quiz.remarks,
                'date_created': quiz.date_created.isoformat(),
                'question_count': len(quiz.questions),
                'chapter': {
                    'id': chapter.id,
                    'name': chapter.name,
                },
                'subject': {
                    'id': subject.id,
                    'name': subject.name,
                }
            }
            return quiz_data, 200
        except Exception as e:
            return {"msg": f"Error retrieving quiz: {str(e)}"}, 500

    def put(self, quiz_id):
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, message="Quiz not found")

            data = request.get_json()
            quiz.name = data.get('name', quiz.name)
            quiz.date_of_quiz = datetime.fromisoformat(data.get('date_of_quiz', quiz.date_of_quiz.isoformat()))
            quiz.due_date = datetime.fromisoformat(data.get('due_date', quiz.due_date.isoformat()))
            quiz.time_duration = datetime.strptime(data.get('time_duration', str(quiz.time_duration)), "%H:%M:%S").time()
            quiz.remarks = data.get('remarks', quiz.remarks)

            db.session.commit()
            return {"msg": "Quiz updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating quiz: {str(e)}"}, 500

    def delete(self, quiz_id):
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, message="Quiz not found")

            db.session.delete(quiz)
            db.session.commit()
            return {"msg": "Quiz deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error deleting quiz: {str(e)}"}, 500
