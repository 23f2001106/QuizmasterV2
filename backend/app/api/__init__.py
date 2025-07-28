from flask import Blueprint
from flask_restful import Api
from .auth.auth_api import *
from .user import *
from .admin import *

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

api.add_resource(LoginResource, '/auth/login')
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(VerifyEmailResource, '/auth/verify-email')
api.add_resource(RequestPasswordResetResource, '/auth/request-password-reset')
api.add_resource(VerifyPasswordResetResource, '/auth/verify-password-reset')
api.add_resource(ResendOtpResource, '/auth/resend-otp')

api.add_resource(UserDashboardResource, '/user/dashboard')
api.add_resource(UserSummaryAnalyticsResource,'/user/summary')
api.add_resource(UserSettingsResource, '/user/settings')
api.add_resource(UserProfileResource,'/user/profile')
api.add_resource(AccountDeletionResource, '/user/account-delete')
api.add_resource(UserQuizListResource, '/user/quizzes')
api.add_resource(UserScoresResource, '/user/scores')
api.add_resource(ExportUserScoresResource, '/user/export')
api.add_resource(ExportJobStatusResource, '/user/export/status')
api.add_resource(ExportDownloadResource, '/user/export/download/<int:job_id>')
api.add_resource(QuizAvailabilityResource, '/user/take_quiz/<int:quiz_id>/availability')
api.add_resource(StartQuizResource, '/user/start_quiz/<int:quiz_id>')
api.add_resource(SubmitQuizResource, '/user/submit_quiz/<int:quiz_id>')
api.add_resource(QuizResultResource, '/user/quiz_result/<int:quiz_id>')

api.add_resource(AdminDashboardResource, '/admin/dashboard')
api.add_resource(AdminSummaryAnalyticsResource, '/admin/summary')
api.add_resource(SubjectListResource, '/admin/subjects')
api.add_resource(SubjectResource, '/admin/subjects/<int:subject_id>')
api.add_resource(AllChaptersResource, '/admin/chapters/all')
api.add_resource(SubjectChapterListResource, '/admin/subjects/<int:subject_id>/chapters')
api.add_resource(ChapterResource, '/admin/chapters/<int:chapter_id>')
api.add_resource(QuizListResource, '/admin/quiz')
api.add_resource(QuizResource, '/admin/quizzes/<int:quiz_id>')
api.add_resource(QuestionListResource, '/admin/quizzes/<int:quiz_id>/questions')
api.add_resource(QuestionResource, '/admin/questions/<int:question_id>')
api.add_resource(UserListResource, '/admin/users')
api.add_resource(UserResource, '/admin/users/<user_id>')
api.add_resource(UserStatusResource, '/admin/users/<user_id>/status')
api.add_resource(AdminSearch, '/admin/search')

def register_api(app):
    app.register_blueprint(api_bp)