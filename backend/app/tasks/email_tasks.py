from app.extensions import celery
from app.utils.email_utils import send_email

def register_email_tasks(celery):
    @celery.task(name='send_verification_email')
    def send_verification_email(user_email, otp, context="register"):
        """
        Send a verification email for registration or password reset.

        """
        subject_map = {
            "register": "Your Registration OTP Code",
            "reset": "Your Password Reset OTP Code",
            "delete": "Your Account Deletion OTP Code"
        }

        template_map = {
            "register": "email_verification.html",
            "reset": "password_reset.html",
            "delete": "delete_account.html"
        }

        subject = subject_map.get(context, "Your OTP Code")
        template_name = template_map.get(context)

        send_email(
            to=user_email,
            subject=subject,
            body=f"Your OTP code is: {otp}",  # fallback text
            template_name=template_name,
            context={"otp": otp}
        )
    return send_verification_email
