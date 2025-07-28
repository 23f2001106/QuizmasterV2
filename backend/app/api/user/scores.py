from flask_restful import Resource
from sqlalchemy.orm import joinedload
from app.decorators import get_current_user_or_abort, verified_and_active_user_required
from app.models import Score, Quiz, Chapter

class UserScoresResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self):
        user = get_current_user_or_abort(require_verified=True)

        try:
            scores = (
                Score.query
                .filter_by(user_id=user.id)
                .options(
                    joinedload(Score.quiz)
                        .joinedload(Quiz.chapter)
                        .joinedload(Chapter.subject),
                    joinedload(Score.quiz)
                        .joinedload(Quiz.questions)
                )
                .order_by(Score.time_stamp_of_attempt.desc())
                .all()
            )

            result = []
            for score in scores:
                quiz = score.quiz
                chapter = quiz.chapter if quiz else None
                subject = chapter.subject if chapter else None

                result.append({
                    "id": score.id,
                    "quiz_id": quiz.id if quiz else None,
                    "quiz_name": quiz.name if quiz else None,
                    "chapter_name": chapter.name if chapter else None,
                    "subject_name": subject.name if subject else None,
                    "time_stamp_of_attempt": score.time_stamp_of_attempt.isoformat() if score.time_stamp_of_attempt else None,
                    "total_scored": score.total_scored,
                    "time_taken": score.time_taken,
                    "total_questions": len(quiz.questions) if quiz and quiz.questions else 0,
                })

            return {"scores": result}, 200

        except Exception as e:
            print(f"Error fetching scores: {e}")
            return {"message": "An error occurred while fetching scores."}, 500
