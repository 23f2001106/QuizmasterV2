from flask import  request
from flask_restful import Resource, abort
from app.models import Quiz
from app.extensions import db
from app.decorators.auth_decorators import admin_required
from datetime import datetime
from app.utils.cache_utils import cache_response, invalidate_cache_for_quizzes, rate_limit


class QuizListResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self):
        try:
            quizzes = Quiz.query.all()
            
            # Explicitly access related data to avoid lazy loading issues
            for quiz in quizzes:
                _ = quiz.chapter.subject
            
            # Manually build the response list
            quizzes_list = []
            for quiz in quizzes:
                quiz_dict = {
                    'id': quiz.id,
                    'name': quiz.name,
                    'date_of_quiz': quiz.date_of_quiz.isoformat() if quiz.date_of_quiz else None,
                    'due_date': quiz.due_date.isoformat() if quiz.due_date else None,
                    'time_duration': quiz.time_duration.isoformat() if quiz.time_duration else None,
                    'remarks': quiz.remarks,
                    'date_created': quiz.date_created.isoformat() if quiz.date_created else None,
                    'questions': [
                        {
                            'id': question.id,
                            'question_statement': question.question_statement
                        } for question in quiz.questions
                    ],
                    'chapter': {
                        'id': quiz.chapter.id,
                        'name': quiz.chapter.name
                    } if quiz.chapter else None,
                    'subject': {
                        'id': quiz.chapter.subject.id,
                        'name': quiz.chapter.subject.name
                    } if quiz.chapter and quiz.chapter.subject else None
                }
                quizzes_list.append(quiz_dict)
            
            return quizzes_list, 200
        
        except Exception as e:
            return {"msg": f"Error retrieving quizzes: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
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

            invalidate_cache_for_quizzes()

            return {"msg": "Quiz created", "id": quiz.id}, 201
        except Exception as e:
            db.session.rollback()
            print("msg:" f"Error creating quiz: {str(e)}")
            return {"msg": f"Error creating quiz: {str(e)}"}, 500

class QuizResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
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

    @rate_limit(limit=50, window=60)
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

            invalidate_cache_for_quizzes()

            return {"msg": "Quiz updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating quiz: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def delete(self, quiz_id):
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, message="Quiz not found")

            db.session.delete(quiz)
            db.session.commit()
            invalidate_cache_for_quizzes()

            return {"msg": "Quiz deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error deleting quiz: {str(e)}"}, 500
