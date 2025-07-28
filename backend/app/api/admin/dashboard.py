from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models import User, Subject, Chapter, Quiz, Question
from app.decorators.auth_decorators import admin_required

class AdminDashboardResource(Resource):
    method_decorators = [admin_required]

    def get(self):
        try:
            # User Stats
            total_users = User.query.filter(User.role != 'admin').count()
            active_users = User.query.filter(User.role != 'admin', User.status == 'active').count()
            suspended_users = User.query.filter(User.role != 'admin', User.status == 'suspended').count()
            verified_users = User.query.filter(User.role != 'admin', User.is_verified == True).count()

            # Content Stats
            total_subjects = Subject.query.count()
            total_chapters = Chapter.query.count()
            total_quizzes = Quiz.query.count()
            total_questions = Question.query.count()

            # Dates
            today = datetime.now().date()
            next_week = today + timedelta(days=7)

            # Recent Items
            recent_quizzes = Quiz.query.order_by(Quiz.date_created.desc()).limit(5).all()
            recent_users = User.query.filter(User.role != 'admin').order_by(User.created_at.desc()).limit(5).all()

            # Upcoming Quizzes
            upcoming_quizzes = Quiz.query.filter(
                Quiz.date_of_quiz.between(today, next_week)
            ).order_by(Quiz.date_of_quiz.asc()).all()

            # Alerts
            unverified_users = User.query.filter(User.role != 'admin', User.is_verified == False).count()
            subjects_without_chapters = Subject.query.outerjoin(Chapter).group_by(Subject.id).having(func.count(Chapter.id) == 0).count()
            chapters_without_quizzes = Chapter.query.outerjoin(Quiz).group_by(Chapter.id).having(func.count(Quiz.id) == 0).count()
            quizzes_past_due = Quiz.query.filter(Quiz.due_date < datetime.now()).count()

            return {
                "stats": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "suspended_users": suspended_users,
                    "verified_users": verified_users,
                    "total_subjects": total_subjects,
                    "total_chapters": total_chapters,
                    "total_quizzes": total_quizzes,
                    "total_questions": total_questions
                },
                "recent_users": [
                    {
                        "id": u.id,
                        "full_name": u.full_name,
                        "username": u.username,
                        "created_at": u.created_at.isoformat()
                    }
                    for u in recent_users
                ],
                "recent_quizzes": [
                    {
                        "id": q.id,
                        "name": q.name,
                        "date_of_quiz": q.date_of_quiz.isoformat(),
                        "subject": q.chapter.subject.name if q.chapter and q.chapter.subject else None
                    }
                    for q in recent_quizzes
                ],
                "upcoming_quizzes": [
                    {
                        "id": q.id,
                        "name": q.name,
                        "date_of_quiz": q.date_of_quiz.isoformat(),
                        "subject": q.chapter.subject.name if q.chapter and q.chapter.subject else None
                    }
                    for q in upcoming_quizzes
                ],
                "alerts": {
                    "unverified_users": unverified_users,
                    "subjects_without_chapters": subjects_without_chapters,
                    "chapters_without_quizzes": chapters_without_quizzes,
                    "quizzes_past_due": quizzes_past_due
                }
            }, 200

        except Exception as e:
            return {"msg": f"Error loading admin dashboard: {str(e)}"}, 500
        