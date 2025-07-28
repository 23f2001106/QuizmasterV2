from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime, timedelta
from app.decorators.auth_decorators import admin_required
from app.models import Quiz, Score, User
from app.extensions import db
from sqlalchemy.orm import joinedload

class AdminSummaryAnalyticsResource(Resource):
    method_decorators = [admin_required]

    def get(self):
        try:
            # Get all scores with related quizzes and questions in one go
            all_scores = db.session.query(Score).options(
                joinedload(Score.quiz).joinedload(Quiz.questions),
                joinedload(Score.user)
            ).all()

            if not all_scores:
                return {
                    "charts": {
                        "average_score_per_subject": [],
                        "highest_score_per_quiz": [],
                        "attempts_per_quiz": [],
                        "attempts_per_day": [],
                        "score_distribution": {"high": 0, "moderate": 0, "low": 0},
                        "attempts_per_subject": [],
                        "user_activity": {
                            "new_users_last_7_days": [],
                            "logins_last_7_days": [],
                            "active_users_last_7_days": 0
                        }
                    },
                    "tables": {"leaderboard": []}
                }, 200

            # --- Helper dicts ---
            subject_scores = {}
            quiz_highest = {}
            quiz_attempts = {}
            score_dist = {"high": 0, "moderate": 0, "low": 0}
            subject_attempts = {}
            leaderboard_stats = {}

            for score in all_scores:
                quiz = score.quiz
                subject = quiz.chapter.subject
                max_score = len(quiz.questions) or 1
                pct_score = (score.total_scored / max_score) * 100

                # 1. Subject-wise percentage scores
                subject_scores.setdefault(subject.name, []).append(pct_score)

                # 2. Highest score per quiz (percentage)
                if quiz.name not in quiz_highest or pct_score > quiz_highest[quiz.name]:
                    quiz_highest[quiz.name] = pct_score

                # 3. Attempts per quiz
                quiz_attempts[quiz.name] = quiz_attempts.get(quiz.name, 0) + 1

                # 4. Score distribution by percentage
                if pct_score >= 80:
                    score_dist["high"] += 1
                elif pct_score >= 50:
                    score_dist["moderate"] += 1
                else:
                    score_dist["low"] += 1

                # 5. Attempts per subject
                subject_attempts[subject.name] = subject_attempts.get(subject.name, 0) + 1

                # 6. Leaderboard percentage aggregation
                if score.user.role != 'admin':
                    leaderboard_stats.setdefault(score.user.id, {
                        "name": score.user.full_name,
                        "username": score.user.username,
                        "scores": []
                    })["scores"].append(pct_score)

            # Format results
            average_score_per_subject = [
                {"label": subj, "value": round(sum(scores) / len(scores), 2)}
                for subj, scores in subject_scores.items()
            ]

            highest_score_per_quiz = [
                {"label": quiz, "value": round(score, 2)}
                for quiz, score in quiz_highest.items()
            ]

            attempts_per_quiz = [
                {"label": quiz, "value": count}
                for quiz, count in quiz_attempts.items()
            ]

            attempts_per_subject = [
                {"label": subject, "value": count}
                for subject, count in subject_attempts.items()
            ]

            # Leaderboard (top 5)
            leaderboard_data = sorted(
                [
                    {
                        "user": data["name"],
                        "username": data["username"],
                        "average_score": round(sum(data["scores"]) / len(data["scores"]), 2),
                        "quizzes_attempted": len(data["scores"])
                    }
                    for data in leaderboard_stats.values()
                ],
                key=lambda x: x["average_score"], reverse=True
            )[:5]

            # --- Attempts Per Day (last 7 days) ---
            last_7_days = datetime.now() - timedelta(days=7)
            daily_attempts = db.session.query(
                func.date(Score.time_stamp_of_attempt),
                func.count(Score.id)
            ).filter(
                Score.time_stamp_of_attempt >= last_7_days
            ).group_by(
                func.date(Score.time_stamp_of_attempt)
            ).order_by(func.date(Score.time_stamp_of_attempt)).all()

            attempts_per_day = [
                {"date": str(date), "value": count}
                for date, count in daily_attempts
            ]

            # --- User Activity Analytics ---
            # 1. New Users Registered (last 7 days)
            new_users = db.session.query(
                func.date(User.created_at),
                func.count(User.id)
            ).filter(User.created_at >= last_7_days).group_by(
                func.date(User.created_at)
            ).order_by(func.date(User.created_at)).all()

            new_users_chart = [
                {"date": str(date), "value": count}
                for date, count in new_users
            ]

            # 2. Active Users (quiz attempts in last 7 days)
            active_users = db.session.query(func.count(
                func.distinct(Score.user_id)
            )).filter(Score.time_stamp_of_attempt >= last_7_days).scalar()

            # 3. Logins Per Day (non-admins)
            daily_logins = db.session.query(
                func.date(User.last_login),
                func.count(User.id)
            ).filter(
                User.last_login >= last_7_days,
                User.role != 'admin'
            ).group_by(
                func.date(User.last_login)
            ).order_by(func.date(User.last_login)).all()

            logins_chart = [
                {"date": str(date), "value": count}
                for date, count in daily_logins
            ]

            user_activity = {
                "new_users_last_7_days": new_users_chart,
                "logins_last_7_days": logins_chart,
                "active_users_last_7_days": active_users or 0
            }

            return {
                "charts": {
                    "average_score_per_subject": average_score_per_subject,
                    "highest_score_per_quiz": highest_score_per_quiz,
                    "attempts_per_quiz": attempts_per_quiz,
                    "attempts_per_day": attempts_per_day,
                    "score_distribution": score_dist,
                    "attempts_per_subject": attempts_per_subject,
                    "user_activity": user_activity
                },
                "tables": {
                    "leaderboard": leaderboard_data
                }
            }, 200

        except Exception as e:
            return {"msg": f"Error generating analytics summary: {str(e)}"}, 500
        