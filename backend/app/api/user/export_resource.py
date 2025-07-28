from flask_restful import Resource
from flask import Response
from app.models import ExportJob, ExportStatus
from app.extensions import db
from flask import current_app
from app.decorators.auth_decorators import verified_and_active_user_required, get_current_user_or_abort

class ExportUserScoresResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def post(self):
        user = get_current_user_or_abort(require_verified=True)
        job = ExportJob(user_id=user.id)
        db.session.add(job)
        db.session.commit()

        current_app.celery.send_task(
            'export_user_scores_csv',
            args=[user.id, job.id]
        )
        return {"message": "Export started", "job_id": job.id}, 202
    
class ExportJobStatusResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self):
        user = get_current_user_or_abort(require_verified=True)
        job = (
            ExportJob.query
            .filter_by(user_id=user.id)
            .order_by(ExportJob.created_at.desc())
            .first()
        )
        if not job:
            return {"status": "none"}

        if job.status == ExportStatus.completed:
            # Return download URL for Redis
            return {
                "status": job.status.value,
                "download_url": f"/user/export/download/{job.id}"
            }

        return {"status": job.status.value}
    

class ExportDownloadResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def get(self, job_id):
        user = get_current_user_or_abort(require_verified=True)

        job = ExportJob.query.filter_by(id=job_id, user_id=user.id, status=ExportStatus.completed).first()
        if not job:
            return {"message": "Export not available"}, 403

        redis_key = f"user_export:{job_id}"
        csv_data = current_app.redis_client.get(redis_key)
        if not csv_data:
            return {"message": "Export expired or not found"}, 404

        csv_str = csv_data.encode('utf-8')

        return Response(
            csv_str,
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=quiz_export_{user.id}.csv"
            }
        )
