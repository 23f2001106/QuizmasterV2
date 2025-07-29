from flask_restful import Resource, abort
from flask import request
from app.models import User, UserStatusEnum, RoleEnum
from app.extensions import db
from app.decorators.auth_decorators import admin_required
from app.utils.cache_utils import cache_response, rate_limit, invalidate_cache_for_users


class UserListResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=120)
    def get(self):
        try:
            users = User.query.filter(User.role != RoleEnum.ADMIN).all()
            formatted_users = []

            for user in users:
                formatted_users.append({
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'qualification': user.qualification,
                    'dob': user.dob.isoformat() if user.dob else None,
                    'role': user.role.value.upper(), 
                    'status': user.status.value.upper(), 
                    'created_at': user.created_at.isoformat(),
                    'last_login': user.last_login.isoformat() if user.last_login else None,
                    'notifications_enabled': user.notifications_enabled,
                    'preferred_reminder_time': user.preferred_reminder_time.strftime('%H:%M'),
                    'is_verified': user.is_verified
                })

            return formatted_users, 200
        except Exception as e:
            return {"msg": f"Error retrieving users: {str(e)}"}, 500


class UserResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    @cache_response(ttl=60)
    def get(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                abort(404, message="User not found")
            return {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'qualification': user.qualification,
                'dob': user.dob.isoformat() if user.dob else None,
                'role': user.role.value.upper(),
                'status': user.status.value.upper(),
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'notifications_enabled': user.notifications_enabled,
                'preferred_reminder_time': user.preferred_reminder_time.strftime('%H:%M'),
                'is_verified': user.is_verified
            }, 200
        
        except Exception as e:
            return {"msg": f"Error retrieving user: {str(e)}"}, 500


class UserStatusResource(Resource):
    method_decorators = [admin_required]

    @rate_limit(limit=100, window=60)
    def put(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                abort(404, message="User not found")

            data = request.get_json()
            new_status = data.get('status')

            if new_status not in UserStatusEnum.__members__:
                return {"msg": "Invalid status. Must be 'ACTIVE' or 'SUSPENDED'"}, 400

            user.status = UserStatusEnum[new_status]
            db.session.commit()

            invalidate_cache_for_users()
            return {"msg": f"User status updated to {new_status}"}, 200

        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error updating user status: {str(e)}"}, 500
