from flask import request, current_app
from flask_restful import Resource
from app.utils.otp_utils import generate_otp
from app.utils.cache_utils import *
from app.extensions import db
from app.decorators import verified_and_active_user_required, get_current_user_or_abort
from datetime import time, datetime


class UserSettingsResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def put(self):
        """Update profile settings"""
        user = get_current_user_or_abort(require_verified=True)
        data = request.json or {}

        full_name = data.get("full_name")
        qualification = data.get("qualification")
        dob = data.get("dob")

        if full_name and not (1 <= len(full_name) <= 100):
            return {"error": "Full name must be between 1 and 100 characters."}, 400

        if dob:
            try:
                dob = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                return {"error": "Invalid date format for DOB. Use YYYY-MM-DD."}, 400

        if full_name:
            user.full_name = full_name
        if qualification is not None:
            user.qualification = qualification
        if dob:
            user.dob = dob

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

    def patch(self):
        """Update notifications and preferred reminder time"""
        user = get_current_user_or_abort(require_verified=True)
        data = request.json or {}
        
        # Toggle or set notifications
        if "notifications_enabled" in data:
            val = data["notifications_enabled"]
            if isinstance(val, bool):
                user.notifications_enabled = val
            elif isinstance(val, str):
                user.notifications_enabled = val.lower() == "true"
            else:
                return {"error": "Invalid value for notifications_enabled."}, 400
        else:
            user.notifications_enabled = not user.notifications_enabled

        # Parse preferred reminder time
        pref_time = data.get("preferred_reminder_time")
        if pref_time:
            try:
                parts = list(map(int, pref_time.split(":")))
                if len(parts) == 2:
                    hour, minute = parts
                elif len(parts) == 3:
                    hour, minute, _ = parts  # Ignore seconds
                else:
                    raise ValueError()
                if not (0 <= hour < 24 and 0 <= minute < 60):
                    raise ValueError()
                user.preferred_reminder_time = time(hour=hour, minute=minute)
            except Exception:
                return {"error": "Invalid time format. Use HH:MM or HH:MM:SS (24-hour)."}, 400

        db.session.commit()
        return {
            "message": "Notification settings updated.",
            "notifications_enabled": user.notifications_enabled,
            "preferred_reminder_time": user.preferred_reminder_time.strftime("%H:%M") if user.preferred_reminder_time else None,
        }, 200


class AccountDeletionResource(Resource):
    method_decorators = [verified_and_active_user_required]

    def post(self):
        """Step 1: Submit password to receive OTP"""
        user = get_current_user_or_abort(require_verified=True)
        data = request.json or {}

        password = data.get("password")
        if not password:
            return {"error": "Password is required."}, 400

        if not user.check_password(password):
            return {"error": "Invalid password."}, 401

        if not can_request_otp(user.id):
            return {
                "error": "OTP already sent. Please wait before requesting again.",
                "retry_after": get_otp_resend_ttl(user.id)
            }, 429

        otp = generate_otp()
        set_otp(user.id, otp)

        current_app.celery.send_task(
            'send_verification_email',
            args=[user.username, otp, 'delete']
        )

        set_resend_otp_lock(user.id)
        
        return {"message": "OTP sent to your email."}, 200

    def delete(self):
        """Step 2: Submit OTP to confirm deletion"""
        user = get_current_user_or_abort(require_verified=True)
        data = request.json or {}
        otp_input = data.get("otp")

        if not otp_input or not otp_input.isdigit() or len(otp_input) != 6:
            return {"error": "Invalid OTP. It must be a 6-digit number."}, 400

        stored_otp = get_otp(user.id)
        if not stored_otp or otp_input != stored_otp:
            return {"error": "Invalid or expired OTP."}, 400

        delete_otp(user.id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "Your account has been deleted."}, 200
