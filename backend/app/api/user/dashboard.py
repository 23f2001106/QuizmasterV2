from flask_restful import Resource
from flask_jwt_extended import  get_jwt_identity
from flask import abort
from app.decorators import verified_and_active_user_required
from app.models import User, Score, Quiz
from datetime import datetime

class UserDashboardResource(Resource):
    method_decorators = [verified_and_active_user_required]
    
    def get(self):
        try:
            user_id = get_jwt_identity()
        except Exception as e:
            print("JWT extraction error:", e)
            abort(422, "Invalid JWT")
        
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")

        scores = Score.query.filter_by(user_id=user_id).all()

        # Upcoming quizzes
        upcoming_quizzes = Quiz.query\
            .filter(Quiz.due_date > datetime.now())\
            .order_by(Quiz.due_date.asc())\
            .limit(3)\
            .all()

        upcoming_data = [{
            "id": quiz.id,
            "name": quiz.name,
            "subject": quiz.chapter.subject.name,
            "date_of_quiz": quiz.date_of_quiz.strftime('%d %b %Y') if quiz.date_of_quiz else None,
            "time_duration": str(quiz.time_duration),
            "question_count": len(quiz.questions),
            "due_date": quiz.due_date.strftime('%d %b %Y') if quiz.due_date else None
        } for quiz in upcoming_quizzes]


        if not scores:
            return {
                "full_name": user.full_name,
                "total_quizzes_attempted": 0,
                "average_score": 0,
                "last_quiz": None,
                "upcoming_quizzes": upcoming_data,
                "performance_breakdown": {
                    "high": 0,
                    "moderate": 0,
                    "low": 0
                }
            }, 200

        total_quizzes_attempted = len(scores)
        percentage_scores = []
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            max_score = len(quiz.questions)
            if max_score > 0:
                percentage = (score.total_scored / max_score) * 100
                percentage_scores.append((score, percentage))
            else:
                percentage_scores.append((score, 0))
                
        average_score = round(sum(p for _, p in percentage_scores) / total_quizzes_attempted, 2)

        # Last quiz info (sorted by time)
        last_score, last_percentage = sorted(percentage_scores, key=lambda x: x[0].time_stamp_of_attempt, reverse=True)[0]
        last_quiz = Quiz.query.get(last_score.quiz_id)

        # Performance breakdown based on percentage
        high = sum(1 for _, p in percentage_scores if p >= 80)
        moderate = sum(1 for _, p in percentage_scores if 40 <= p < 80)
        low = sum(1 for _, p in percentage_scores if p < 40)

        performance_breakdown = {
            "high": high,
            "moderate": moderate,
            "low": low
        }

        return {
            "full_name": user.full_name,
            "total_quizzes_attempted": total_quizzes_attempted,
            "average_score": average_score,
            "last_quiz": {
                "quiz_name": last_quiz.name,
                "score": round(last_percentage, 2),
                "date": last_score.time_stamp_of_attempt.strftime('%d %b %Y') if last_score.time_stamp_of_attempt else None
            },
            "upcoming_quizzes": upcoming_data,
            "performance_breakdown": performance_breakdown
        }