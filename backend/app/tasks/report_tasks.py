from calendar import monthrange
from datetime import datetime
from app.models import User, Quiz, Score
from app.utils.pdf_utils import generate_pdf_from_template
from app.utils.email_utils import send_email
from app.extensions import db
import logging

logger = logging.getLogger(__name__)

def register_report_tasks(celery):
    @celery.task(name="send_monthly_report")
    def send_monthly_report(force=False):
        logger.info("send_monthly_report task triggered")
        now = datetime.now()
        last_day = monthrange(now.year, now.month)[1]
        logger.info(f"Task started at {now}, last day of month is {last_day}")

        # Only send report on the last day of the month
        if not force and now.day != last_day:
            logger.info("Not last day of month, exiting.")
            return

        month_start = datetime(now.year, now.month, 1)
        month_end = datetime(now.year, now.month, last_day, 23, 59, 59)

        users = User.query.filter_by(is_verified=True, status='active', role ='user').all()
        print(f"Found {len(users)} users")

        for user in users:
            
            scores = (
                db.session.query(Quiz, Score)
                .join(Score, (Score.quiz_id == Quiz.id))
                .filter(
                    Score.user_id == user.id,
                    Quiz.date_of_quiz >= month_start,
                    Quiz.date_of_quiz <= month_end
                )
                .all()
            )

            quizzes_list = []
            total_score = 0
            for quiz, score_obj in scores:
                quizzes_list.append({
                    "name": quiz.name,
                    "date": score_obj.time_stamp_of_attempt.strftime("%Y-%m-%d"),
                    "score": score_obj.total_scored,
                })
                total_score += score_obj.total_scored

            total_quizzes = len(quizzes_list)
            average_score = round(total_score / total_quizzes, 2) if total_quizzes > 0 else 0

            context = {
                "username": user.full_name,
                "month": now.strftime("%B %Y"),
                "quizzes": quizzes_list,
                "total_quizzes": total_quizzes,
                "average_score": average_score,
            }
            attachments = []
            try:
                pdf_bytes = generate_pdf_from_template("monthly_report.html", context)
                attachments.append(("monthly_report.pdf", pdf_bytes, "application/pdf"))

            except Exception as e:
                print(f"Failed to generate PDF for user {user.username}: {e}")
            
            send_email(
                to=user.username,
                subject=f"Your Monthly Quiz Report - {context['month']}",
                template_name="monthly_report.html",
                context=context,
                attachments=attachments if attachments else None
            )

    return send_monthly_report