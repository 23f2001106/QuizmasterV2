from flask_restful import Resource
from app.decorators.auth_decorators import *

from datetime import time

class UserProfileResource(Resource):
    @verified_and_active_user_required
    def get(self):
        user = get_current_user_or_abort()

        def safe_iso(dt):
            return dt.isoformat() if dt else None

        def time_to_str(t):
            return t.strftime('%H:%M:%S') if isinstance(t, time) else None

        return {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "qualification": user.qualification or None,
            "dob": safe_iso(user.dob),
            "role": user.role.value,
            "status": user.status.value,
            "is_verified": user.is_verified,
            "notifications_enabled": user.notifications_enabled,
            "preferred_reminder_time": time_to_str(user.preferred_reminder_time),
            "created_at": safe_iso(user.created_at),
            "last_login": safe_iso(user.last_login),
        }

