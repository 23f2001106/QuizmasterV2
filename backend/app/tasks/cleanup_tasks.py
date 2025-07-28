from datetime import datetime, timedelta

from app.extensions import db
from app.models import User

def register_cleanup_tasks(celery):
    @celery.task(name='delete_unverified_users_older_than')
    def delete_unverified_users_older_than(hours=24):
        expiry_time = datetime.now() - timedelta(hours=hours)
        old_users = User.query.filter(
            User.is_verified == False,
            User.created_at < expiry_time
        ).all()

        for user in old_users:
            db.session.delete(user)
        db.session.commit()

    return delete_unverified_users_older_than

