import csv
from io import StringIO
from flask import current_app
from app.extensions import  db
from app.models import Score, User, ExportJob, Quiz, Chapter, ExportStatus
from sqlalchemy.orm import joinedload
from datetime import datetime

def register_export_tasks(celery):
    @celery.task(name="export_user_scores_csv")
    def export_user_scores_csv(user_id, job_id):
        try:
            job = db.session.get(ExportJob, job_id)
            user = db.session.get(User, user_id)
            if not user:
                job.status = ExportStatus.failed
                db.session.commit()
                return {"error": "User not found"}

            scores = (
                Score.query
                .filter_by(user_id=user.id)
                .options(
                    joinedload(Score.quiz).joinedload(Quiz.chapter).joinedload(Chapter.subject),
                    joinedload(Score.quiz).joinedload(Quiz.questions)
                )
                .order_by(Score.time_stamp_of_attempt.desc())
                .all()
            )

            output = StringIO()
            writer = csv.writer(output)
            writer.writerow([
                "quiz_id", "quiz_name", "chapter_id", "chapter_name", "subject_name",
                "date_of_quiz", "total_scored", "total_questions", "score_percentage", "remarks"
            ])

            for score in scores:
                quiz = score.quiz
                chapter = quiz.chapter
                subject = chapter.subject
                total_q = len(quiz.questions)
                percentage = (score.total_scored / total_q * 100) if total_q else 0
                remarks = "Good attempt" if percentage >= 75 else "Needs improvement"
                writer.writerow([
                    quiz.id,
                    quiz.name,
                    chapter.id,
                    chapter.name,
                    subject.name,
                    score.time_stamp_of_attempt.strftime("%Y-%m-%d"),
                    score.total_scored,
                    total_q,
                    round(percentage, 2),
                    remarks
                ])

            csv_content = output.getvalue()

            redis_key = f"user_export:{job_id}"
            current_app.redis_client.set(redis_key, csv_content, ex=3600)  # expires in 1 hour

            job.filename = None
            job.status = ExportStatus.completed
            job.completed_at = datetime.now()
            db.session.commit()

            return {"status": "completed"}

        except Exception as e:
            job = db.session.get(ExportJob, job_id)
            if job:
                job.status = ExportStatus.failed
                db.session.commit()
            current_app.logger.error(f"Export failed: {e}")
            return {"error": str(e)}
        
    return export_user_scores_csv