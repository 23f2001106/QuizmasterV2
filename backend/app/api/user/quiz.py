from flask_restful import Resource
from app.models import Quiz, Chapter
from app.decorators import get_current_user_or_abort, verified_and_active_user_required
from sqlalchemy.orm import joinedload

class UserQuizListResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self):
        user = get_current_user_or_abort()
        quizzes = (
            Quiz.query
            .options(
                joinedload(Quiz.chapter).joinedload(Chapter.subject)
            )
            .all()
        )

        result = []
        for quiz in quizzes:
            chapter = quiz.chapter
            subject = chapter.subject if chapter else None

            result.append({
                "id": quiz.id,
                "name": quiz.name,
                "date_of_quiz": quiz.date_of_quiz.strftime('%d %b %Y') if quiz.date_of_quiz else None,
                "due_date": quiz.due_date.strftime('%d %b %Y') if quiz.due_date else None,
                "time_duration": str(quiz.time_duration) if quiz.time_duration else None,
                "remarks": quiz.remarks,
                "chapter_name": chapter.name if chapter else None,
                "subject_name": subject.name if subject else None,
            })

        return result, 200


