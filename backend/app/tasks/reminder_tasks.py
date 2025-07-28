from datetime import datetime, timedelta, time, date
from flask import current_app
from app.extensions import db
from app.models import User, Quiz, ReminderLog
from app.utils.email_utils import send_email

DEFAULT_REMINDER_TIME = time(hour=18, minute=0)  # 6 PM

def register_reminder_tasks(celery):
    @celery.task(name="send_daily_reminders")
    def send_daily_reminders(force_send=False):
        now = datetime.now()
        today = date.today()

        base_url = current_app.config.get('BASE_URL', 'http://localhost:8080')

        users = User.query.filter_by(is_verified=True, status='active').all()

        for user in users:
            if user.is_admin():
                continue

            if not user.notifications_enabled:
                continue

            preferred_time = user.preferred_reminder_time or DEFAULT_REMINDER_TIME

            if not force_send and now.time() < preferred_time:
                continue

            sent_today = ReminderLog.query.filter_by(user_id=user.id, reminder_date=today).first()
            if sent_today and not force_send:
                continue

            threshold = now - timedelta(days=1)
            recent_login = user.last_login and user.last_login > threshold

            attempted_quiz_ids = {score.quiz_id for score in user.scores}
            new_quizzes = Quiz.query.filter(~Quiz.id.in_(attempted_quiz_ids)).order_by(Quiz.date_of_quiz.desc()).all()

            if not recent_login or new_quizzes:
                quiz = new_quizzes[0] if new_quizzes else None

                context = {
                    "username": user.full_name,
                    "quiz_title": quiz.name if quiz else "your pending quizzes",
                    "due_date": quiz.due_date.strftime("%B %d, %Y") if quiz else "soon",
                    "quiz_url": f"{base_url}/user/quizzes"
                }

                send_email(
                    to=user.username,
                    subject="Reminder: Don't miss your next quiz!",
                    template_name="daily_reminder.html",
                    context=context
                )

                reminder_log = ReminderLog(user_id=user.id, reminder_date=today)
                db.session.add(reminder_log)
                db.session.commit()

    return send_daily_reminders
