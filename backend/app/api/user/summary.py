from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.models import User, Score
from app.extensions import db
from app.decorators import verified_and_active_user_required


class UserSummaryAnalyticsResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self):
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt).all()

            if not scores:
                return jsonify({
                    "full_name": user.full_name,
                    "score_trend": [],
                    "score_distribution": {"high": 0, "moderate": 0, "low": 0},
                    "subject_performance": [],
                    "most_attempted_subject": None,
                    "average_time_per_quiz": 0,
                    "attempts_per_subject": [],
                    "best_subject": None,
                    "weak_subject": None,
                    "weekly_attempts": [],
                    "user_rank": None,
                    "leaderboard": []
                })

            # Score Trend
            score_trend = []
            percentage_scores = []
            subject_stats = {}
            high = moderate = low = 0
            total_time = 0

            for s in scores:
                quiz = s.quiz
                max_score = len(quiz.questions) or 1
                percentage = (s.total_scored / max_score) * 100
                percentage_scores.append((s, percentage))

                # Trend
                score_trend.append({
                    "date": s.time_stamp_of_attempt.date().isoformat(),
                    "score": round(percentage, 2)
                })

                # Distribution
                if percentage >= 80:
                    high += 1
                elif percentage >= 40:
                    moderate += 1
                else:
                    low += 1

                # Subject performance
                subject = quiz.chapter.subject
                if subject.id not in subject_stats:
                    subject_stats[subject.id] = {
                        "name": subject.name,
                        "total_percentage": 0,
                        "count": 0
                    }
                subject_stats[subject.id]["total_percentage"] += percentage
                subject_stats[subject.id]["count"] += 1

                # Time
                total_time += s.time_taken

            score_distribution = {"high": high, "moderate": moderate, "low": low}

            subject_performance = [
                {
                    "label": data["name"],
                    "value": round(data["total_percentage"] / data["count"], 2)
                }
                for data in subject_stats.values()
            ]

            best_subject = max(subject_stats.items(), key=lambda x: x[1]["total_percentage"] / x[1]["count"])[1]["name"]
            weak_subject = min(subject_stats.items(), key=lambda x: x[1]["total_percentage"] / x[1]["count"])[1]["name"]
            most_attempted_subject = max(subject_stats.items(), key=lambda x: x[1]["count"])[1]["name"]

            average_time = round(total_time / len(scores), 2)

            attempts_per_subject = [
                {"label": data["name"], "value": data["count"]}
                for data in subject_stats.values()
            ]

            # Weekly Attempts
            seven_days_ago = datetime.now() - timedelta(days=7)
            weekly_attempts_query = Score.query.filter(
                Score.user_id == user_id,
                Score.time_stamp_of_attempt >= seven_days_ago
            ).with_entities(
                func.date(Score.time_stamp_of_attempt),
                func.count(Score.id)
            ).group_by(func.date(Score.time_stamp_of_attempt)).order_by(func.date(Score.time_stamp_of_attempt)).all()

            weekly_attempts = [
                {"date": str(date), "value": count}
                for date, count in weekly_attempts_query
            ]

            # User Rank (average percentage-based)
            all_user_scores = Score.query.join(User).filter(User.role != "admin").all()
            user_avg_percent = {}

            for s in all_user_scores:
                quiz = s.quiz
                max_score = len(quiz.questions) or 1
                pct = (s.total_scored / max_score) * 100
                user_avg_percent.setdefault(s.user_id, []).append(pct)

            user_avg_percent = {
                uid: sum(pcts) / len(pcts)
                for uid, pcts in user_avg_percent.items()
            }

            sorted_users = sorted(user_avg_percent.items(), key=lambda x: x[1], reverse=True)
            user_rank = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == user_id), None)

            # Leaderboard Top 5
            leaderboard = []
            user_in_top_5 = False

            for i, (uid, avg_score) in enumerate(sorted_users[:5]):
                quiz_count = sum(1 for s in all_user_scores if s.user_id == uid)
                name = User.query.get(uid).full_name
                entry = {
                    "rank": i + 1,
                    "user": name,
                    "average_score": round(avg_score, 2),
                    "quizzes_attempted": quiz_count,
                    "is_you": uid == user_id
                }
                if uid == user_id:
                    user_in_top_5 = True
                leaderboard.append(entry)

            # Append user's own rank if not in top 5
            if not user_in_top_5 and user_rank:
                avg_score = round(user_avg_percent[user_id], 2)
                quiz_count = len([s for s in all_user_scores if s.user_id == user_id])
                leaderboard.append({
                    "rank": user_rank,
                    "user": user.full_name,
                    "average_score": avg_score,
                    "quizzes_attempted": quiz_count,
                    "is_you": True
                })

            return jsonify({
                "full_name": user.full_name,
                "score_trend": score_trend,
                "score_distribution": score_distribution,
                "subject_performance": subject_performance,
                "most_attempted_subject": most_attempted_subject,
                "average_time_per_quiz": average_time,
                "attempts_per_subject": attempts_per_subject,
                "best_subject": best_subject,
                "weak_subject": weak_subject,
                "weekly_attempts": weekly_attempts,
                "user_rank": user_rank,
                "leaderboard": leaderboard
            })

        except Exception as e:
            return {"msg": f"Error generating user summary: {str(e)}"}, 500
