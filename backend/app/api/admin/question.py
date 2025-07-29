from flask_restful import Resource, abort
from flask import request
from app.models import Question, Quiz
from app.extensions import db
from app.decorators.auth_decorators import admin_required
from app.utils.cache_utils import cache_response, rate_limit, invalidate_cache_for_questions


class QuestionListResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self, quiz_id):
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, message="Quiz not found")

            questions_data = [
                {
                    "id": q.id,
                    "question_statement": q.question_statement,
                    "option1": q.option1,
                    "option2": q.option2,
                    "option3": q.option3,
                    "option4": q.option4,
                    "correct_option": q.correct_option,
                    "quiz_id": q.quiz_id
                } for q in quiz.questions
            ]
            return questions_data, 200
        except Exception as e:
            return {"msg": f"Error retrieving questions: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def post(self, quiz_id):
        try:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                abort(404, message="Quiz not found")

            data = request.get_json()
            required_fields = ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
            if not all(field in data for field in required_fields):
                return {"msg": "Missing required fields"}, 400

            question = Question(
                quiz_id=quiz_id,
                question_statement=data['question_statement'],
                option1=data['option1'],
                option2=data['option2'],
                option3=data['option3'],
                option4=data['option4'],
                correct_option=data['correct_option']
            )

            db.session.add(question)
            db.session.commit()
            invalidate_cache_for_questions(quiz_id=quiz_id)

            return {"msg": "Question created", "id": question.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error creating question: {str(e)}"}, 500

class QuestionResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self, question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404, message="Question not found")

            question_data = {
                "id": question.id,
                "question_statement": question.question_statement,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
                "correct_option": question.correct_option,
                "quiz_id": question.quiz_id
            }
            return question_data, 200
        except Exception as e:
            return {"msg": f"Error retrieving question: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def put(self, question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404, message="Question not found")

            quiz_id = question.quiz_id

            data = request.get_json()
            question.question_statement = data.get('question_statement', question.question_statement)
            question.option1 = data.get('option1', question.option1)
            question.option2 = data.get('option2', question.option2)
            question.option3 = data.get('option3', question.option3)
            question.option4 = data.get('option4', question.option4)
            question.correct_option = data.get('correct_option', question.correct_option)

            db.session.commit()
            invalidate_cache_for_questions(quiz_id=quiz_id)
            return {"msg": "Question updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating question: {str(e)}"}, 500

    @rate_limit(limit=50, window=60)
    def delete(self, question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404, message="Question not found")

            quiz_id = question.quiz_id
            db.session.delete(question)
            db.session.commit()
            invalidate_cache_for_questions(quiz_id=quiz_id)
            return {"msg": "Question deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error deleting question: {str(e)}"}, 500
