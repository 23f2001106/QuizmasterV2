from flask_restful import Resource, abort
from flask import request
from datetime import datetime
from app.extensions import db
from app.models import Quiz, Score
from app.decorators import verified_and_active_user_required, get_current_user_or_abort

class QuizAvailabilityResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)

        if not quiz:
            abort(404, message="Quiz not found")

        now = datetime.now()

        if now < quiz.date_of_quiz:
            return {
                "status": "upcoming",
                "message": f"This quiz will be available on {quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S')}"
            }, 200

        elif now > quiz.due_date:
            return {
                "status": "expired",
                "message": f"The quiz expired on {quiz.due_date.strftime('%Y-%m-%d %H:%M:%S')}"
            }, 200

        else:
            general_instructions = [
                "This is a multiple choice quiz with 4 options per question.",
                "Only one option is correct per question.",
                "A countdown timer is displayed at the top right corner.",
                "The quiz is automatically submitted when the timer runs out.",
                "Click 'Next' to go to the next question.",
                "Click 'Previous' to navigate to the previous question.",
                "Click 'Clear' to remove the selected answer for a question."
            ]

            total_marks = len(quiz.questions)

            return {
                "status": "available",
                "general_instructions": general_instructions,
                "quiz_details": {
                    "quiz_id": quiz.id,
                    "quiz_name": quiz.name,
                    "total_marks": total_marks,
                    "time_duration": str(quiz.time_duration),
                    "remarks": quiz.remarks
                }
            }, 200


class StartQuizResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)

        if not quiz:
            abort(404, message="Quiz not found")

        now = datetime.now()

        if now < quiz.date_of_quiz:
            abort(400, message="Quiz not yet available")
        if now > quiz.due_date:
            abort(400, message="Quiz has expired")

        questions_payload = [
            {
                "serial_number": idx + 1,
                "id": q.id,
                "question_statement": q.question_statement,
                "options": [
                    {"value": 1, "text": q.option1},
                    {"value": 2, "text": q.option2},
                    {"value": 3, "text": q.option3},
                    {"value": 4, "text": q.option4}
                ]
            }
            for idx, q in enumerate(quiz.questions)
        ]

        return {
            "status": "available",
            "quiz_id": quiz.id,
            "quiz_name": quiz.name,
            "time_duration": str(quiz.time_duration),
            "start_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "questions": questions_payload
        }, 200
    

class SubmitQuizResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def post(self, quiz_id):
        user = get_current_user_or_abort(require_verified=True)
        quiz = Quiz.query.get(quiz_id)

        if not quiz:
            abort(404, message="Quiz not found")

        data = request.get_json(force=True)  

        if not data:
            abort(400, message="Missing JSON data")

        user_answers = data.get('answers')
        time_taken = data.get('time_taken')

        if user_answers is None or not isinstance(user_answers, list):
            abort(400, message="'answers' field is required and must be a list")

        if time_taken is None or not isinstance(time_taken, (int, float)):
            abort(400, message="'time_taken' field is required and must be a number")


        question_map = {q.id: q for q in quiz.questions}
        total_questions = len(question_map)
        correct_count = 0

        for ans in user_answers:
            qid = ans.get('question_id')
            selected_option = ans.get('selected_option')
            if not qid or qid not in question_map:
                continue

            if selected_option not in [1, 2, 3, 4]:
                continue

            if question_map[qid].correct_option == selected_option:
                correct_count += 1

        score_entry = Score(
            quiz_id=quiz.id,
            user_id=user.id,
            total_scored=correct_count,
            time_taken=time_taken,
            time_stamp_of_attempt=datetime.now()
        )

        db.session.add(score_entry)
        db.session.commit()

        return {
            "message": "Quiz submitted successfully",
            "score_summary": {
                "total_questions": total_questions,
                "attempted": len(user_answers),
                "correct_answers": correct_count,
                "wrong_answers": len(user_answers) - correct_count,
                "total_scored": correct_count,
                "time_taken_seconds": time_taken
            }
        }, 200
    
class QuizResultResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self, quiz_id):
        user = get_current_user_or_abort(require_verified=True)
        quiz = Quiz.query.get(quiz_id)

        if not quiz:
            abort(404, message="Quiz not found")

        score = Score.query.filter_by(user_id=user.id, quiz_id=quiz.id)\
                           .order_by(Score.time_stamp_of_attempt.desc()).first()

        if not score:
            abort(404, message="No submission found for this quiz")

        total_questions = len(quiz.questions)
        scored = score.total_scored
        percentage = (scored / total_questions) * 100 if total_questions > 0 else 0

        time_taken_seconds = int(score.time_taken)
        mins, secs = divmod(time_taken_seconds, 60)
        time_taken_str = f"{mins} mins {secs} secs" if mins else f"{secs} secs"

        if percentage >= 90:
            message = "Excellent work!"
        elif percentage >= 75:
            message = "Great job!"
        elif percentage >= 50:
            message = "Good effort!"
        else:
            message = "Keep practicing!"

        return {
            "quiz_id": quiz.id,
            "quiz_name": quiz.name,
            "score": f"{scored}/{total_questions}",
            "percentage": round(percentage, 2),
            "time_taken": time_taken_str,
            "message": message,
            "attempted_on": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M:%S")
        }, 200
    
    