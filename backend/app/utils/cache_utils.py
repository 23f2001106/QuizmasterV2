from flask import current_app


def get_redis():
    redis = getattr(current_app, 'redis_client', None)
    if redis is None:
        raise RuntimeError("Redis client not initialized in app context.")
    return redis


OTP_EXPIRY = 300  
RESEND_OTP_COOLDOWN = 60  
TEMP_PASSWORD_EXPIRY = 300  

# OTP Functions
def set_otp(user_id, otp, expiry=OTP_EXPIRY):
    key = f"email_otp:{user_id}"
    get_redis().setex(key, expiry, otp)

def get_otp(user_id):
    key = f"email_otp:{user_id}"
    return get_redis().get(key)

def delete_otp(user_id):
    key = f"email_otp:{user_id}"
    get_redis().delete(key)

# Temporary Password Functions
def set_temp_password(user_id, password, expiry=TEMP_PASSWORD_EXPIRY):
    key = f"reset_pass:{user_id}"
    get_redis().setex(key, expiry, password)

def get_temp_password(user_id):
    key = f"reset_pass:{user_id}"
    return get_redis().get(key)

def delete_temp_password(user_id):
    key = f"reset_pass:{user_id}"
    get_redis().delete(key)

# Resend Lock Functions
def can_request_otp(user_id):
    key = f"email_otp:{user_id}"
    return not get_redis().exists(key)

def get_otp_resend_ttl(user_id):
    key = f"resend_otp_lock:{user_id}"
    return get_redis().ttl(key)

def set_resend_otp_lock(user_id, cooldown=RESEND_OTP_COOLDOWN):  
    key = f"resend_otp_lock:{user_id}"
    get_redis().setex(key, cooldown, "locked")
