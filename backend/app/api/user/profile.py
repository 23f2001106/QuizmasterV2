from flask_restful import Resource
from app.decorators.auth_decorators import *
from app.utils.cache_utils import cache_response, rate_limit

from datetime import time

class UserProfileResource(Resource):
    method_decorators = [verified_and_active_user_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=60, user_scope=True)
    def get(self):
        user = get_current_user_or_abort()

        def time_to_str(t):
            return t.strftime('%H:%M:%S') if isinstance(t, time) else None

        return {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "qualification": user.qualification or None,
            "dob": user.dob.strftime('%Y-%m-%d') if user.dob else None,
            "role": user.role.value,
            "status": user.status.value,
            "is_verified": user.is_verified,
            "notifications_enabled": user.notifications_enabled,
            "preferred_reminder_time": time_to_str(user.preferred_reminder_time),
            "created_at": user.created_at.strftime('%Y-%m-%d'),
            "last_login": user.last_login.strftime('%Y-%m-%d'),
        }, 200

