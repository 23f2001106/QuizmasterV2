from flask_restful import Resource, reqparse
from app.models import User, Subject, Quiz
from app.decorators.auth_decorators import admin_required
from sqlalchemy.orm import subqueryload

class AdminSearch(Resource):
    method_decorators = [admin_required]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category', type=str, location='args', required=True, help="Category is required")
        parser.add_argument('query', type=str, location='args', required=True, help="Query is required")
        args = parser.parse_args()

        category = args['category'].lower()
        query = args['query'].strip().lower()

        results = []

        if category == "users":
            users = User.query.filter(
                (User.username.ilike(f'%{query}%')) | 
                (User.full_name.ilike(f'%{query}%'))
            ).all()
            results = [
                {
                    "id": u.id,
                    "username": u.username,
                    "full_name": u.full_name,
                    "role": u.role,
                    "status": u.status,
                    "is_verified": u.is_verified
                }
                for u in users
            ]

        elif category == "subjects":
            subjects = Subject.query.filter(
                Subject.name.ilike(f"%{query}%")
            ).all()
            results = [
                {
                    "id": s.id,
                    "name": s.name,
                    "level": s.level
                }
                for s in subjects
            ]

        elif category == "quizzes":
            quizzes = Quiz.query.options(subqueryload(Quiz.questions)).filter(
                Quiz.name.ilike(f"%{query}%")
            ).all()
            results = [
                {
                    "id": q.id,
                    "name": q.name,
                    "chapter_id": q.chapter_id,
                    "date_of_quiz": q.date_of_quiz.strftime("%Y-%m-%d") if q.date_of_quiz else None,
                    "due_date": q.due_date.strftime("%Y-%m-%d") if q.due_date else None,
                    "time_duration": q.time_duration.strftime("%H:%M:%S") if q.time_duration else None,
                    "question_count": len(q.questions)
                }
                for q in quizzes
            ]
        else:
            return {"error": "Invalid category"}, 400

        return {"results": results}, 200
