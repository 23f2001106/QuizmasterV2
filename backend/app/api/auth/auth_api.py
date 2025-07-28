from flask import current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from datetime import datetime

from app.models import User, UserStatusEnum
from app.extensions import db
from app.utils.otp_utils import generate_otp
from app.utils.cache_utils import *


login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        username = args['username'].strip().lower()
        password = args['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid username or password"}, 401

        if not user.is_active():
            return {"message": "Account is suspended"}, 403

        if not user.is_verified or user.status != UserStatusEnum.ACTIVE:
            return {
                "message": "Account not active or email not verified."
            }, 403

        access_token = create_access_token(identity=str(user.id))
        response = {
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "name": user.full_name,
                    "username": user.username,
                    "role": user.role.value,
                },
            }

        user.last_login = datetime.now()
        db.session.commit()

        return response, 200
    
register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True, help="Username (email) is required")
register_parser.add_argument('password', type=str, required=True, help="Password is required")
register_parser.add_argument('full_name', type=str, required=True, help="Full name is required")
register_parser.add_argument('qualification', type=str)
register_parser.add_argument('dob', type=str)


class RegisterResource(Resource):
    def get(self):
        return {"message": "Register endpoint - use POST to create user."}
    def post(self):
        args = register_parser.parse_args()
        username = args['username'].strip().lower()
        password = args['password']
        full_name = args['full_name']
        qualification = args.get('qualification')
        dob = args.get('dob')

        if User.query.filter_by(username=username).first():
            return {"message": "User already exists"}, 400

        user = User(
            username=username,
            full_name=full_name,
            qualification=qualification,
            dob=datetime.strptime(dob, '%Y-%m-%d') if dob else None,
            is_verified=False
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        otp = generate_otp()
        set_otp(user.id, otp)

        current_app.celery.send_task(
            'send_verification_email',
            args=[user.username, otp]
        )

        return {
            "message": "User registered successfully",
            "user_id": user.id
        }, 201
    
verify_parser = reqparse.RequestParser()
verify_parser.add_argument('user_id', type=int, required=True)
verify_parser.add_argument('otp', type=str, required=True)

class VerifyEmailResource(Resource):
    def post(self):
        args = verify_parser.parse_args()
        user_id = args['user_id']
        otp = args['otp']

        stored_otp = get_otp(user_id)
        if not stored_otp:
            return {"message": "OTP expired or invalid."}, 400

        if stored_otp != otp:
            return {"message": "Invalid OTP."}, 400

        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found."}, 404

        user.is_verified = True
        user.status = UserStatusEnum.ACTIVE
        db.session.commit()
        delete_otp(user_id)

        return {"message": "Email verified successfully."}, 200
    
reset_request_parser = reqparse.RequestParser()
reset_request_parser.add_argument('username', type=str, required=True, help="Username (email) is required")
reset_request_parser.add_argument('new_password', type=str, required=True)
reset_request_parser.add_argument('confirm_password', type=str, required=True)

class RequestPasswordResetResource(Resource):
    def post(self):
        args = reset_request_parser.parse_args()
        username = args['username'].strip().lower()
        new_password = args['new_password']
        confirm_password = args['confirm_password']

        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, 404

        if new_password != confirm_password:
            return {"message": "Passwords do not match"}, 400

        if user.check_password(new_password):
            return {"message": "New password cannot be the same as the old password"}, 400

        # Temporarily store new password (can use Redis)
        set_temp_password(user.id, new_password)

        # Generate and send OTP
        otp = generate_otp()
        set_otp(user.id, otp)
        current_app.celery.send_task(
            'send_verification_email',
            args=[user.username, otp, 'reset']
        )

        return {"message": "OTP sent to your email for password reset verification",
                "user_id": user.id
                }, 200

verify_reset_parser = reqparse.RequestParser()
verify_reset_parser.add_argument('user_id', type=int, required=True)
verify_reset_parser.add_argument('otp', type=str, required=True)

class VerifyPasswordResetResource(Resource):
    def post(self):
        args = verify_reset_parser.parse_args()
        user_id = args['user_id']
        otp = args['otp']

        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        stored_otp = get_otp(user_id)
        if not stored_otp or stored_otp != otp:
            return {"message": "Invalid or expired OTP"}, 400

        new_password = get_temp_password(user_id)
        if not new_password:
            return {"message": "Reset request expired or invalid"}, 400

        user.set_password(new_password)
        db.session.commit()

        delete_otp(user_id)
        delete_temp_password(user_id)

        return {"message": "Password reset successful"}, 200
    
resend_otp_parser = reqparse.RequestParser()
resend_otp_parser.add_argument('user_id', type=int, required=True)
resend_otp_parser.add_argument('context', type=str, choices=('register', 'reset', 'delete'), required=True)

class ResendOtpResource(Resource):
    def post(self):
        args = resend_otp_parser.parse_args()
        user_id = args['user_id']
        context = args['context']

        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found."}, 404

        if not can_request_otp(user_id):
            ttl = get_otp_resend_ttl(user_id)
            if ttl < 0:
                ttl = 60
            return {
                "message": f"Please wait {ttl} seconds before requesting another OTP.",
                "cooldown": ttl
            }, 429
        
        # Only allow resend in valid states
        if context == 'register' and user.is_verified:
            return {"message": "User already verified."}, 400

        if context == 'reset' and not get_temp_password(user_id):
            return {"message": "No password reset in progress for this user."}, 400

        if context == 'delete':
            if not user.is_verified:
                return {"message": "User must be verified to delete account."}, 400

        otp = generate_otp()
        set_otp(user.id, otp)

        current_app.celery.send_task(
            'send_verification_email',
            args=[user.username, otp, context]
        )
        set_resend_otp_lock(user.id)

        return {"message": "OTP resent successfully."}, 200
