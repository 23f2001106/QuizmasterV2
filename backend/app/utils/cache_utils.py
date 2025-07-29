from flask import current_app, request, make_response
from functools import wraps
import json
from app.decorators import get_current_user_or_abort

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


# --- Caching & Rate Limiting ---

def cache_response(ttl=60, user_scope=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            redis = get_redis()
            if user_scope:
                user = get_current_user_or_abort()
                cache_key = f"cache:{request.path}:user:{user.id}:{str(sorted(request.args.items()))}"
            else:
                cache_key = f"cache:{request.path}:{str(sorted(request.args.items()))}"

            cached = redis.get(cache_key)
            print("Cache key:", cache_key, "Cache hit:", bool(cached))

            if cached:
                return make_response(json.loads(cached), 200)
            result = func(*args, **kwargs)

            if isinstance(result, tuple):
                response, status = result
            else:
                response, status = result, 200

            if status == 200:
                redis.setex(cache_key, ttl, json.dumps(response))

            return make_response(response, status)
        return wrapper
    return decorator

def invalidate_cache_by_prefix(prefix):
    redis = get_redis()
    cursor = 0
    while True:
        cursor, keys = redis.scan(cursor=cursor, match=f"{prefix}*")
        if keys:
            keys = [k.decode('utf-8') if isinstance(k, bytes) else k for k in keys]
            redis.delete(*keys)
        if cursor == 0:
            break

def invalidate_cache_for_subjects():
    invalidate_cache_by_prefix("cache:/api/admin/subjects")

def invalidate_cache_for_chapters():
    invalidate_cache_by_prefix("cache:/api/admin/chapters")
    invalidate_cache_by_prefix("cache:/api/admin/subjects")

def invalidate_cache_for_quizzes():
    invalidate_cache_by_prefix("cache:/api/admin/quiz")
    invalidate_cache_by_prefix("cache:/api/admin/quizzes")

def invalidate_cache_for_questions(quiz_id=None):
    invalidate_cache_by_prefix("cache:/api/admin/questions")

    if quiz_id is not None:
        invalidate_cache_by_prefix(f"cache:/api/admin/quizzes/{quiz_id}/questions")

    invalidate_cache_by_prefix("cache:/api/admin/quizzes")
    invalidate_cache_by_prefix("cache:/api/admin/quiz")

def invalidate_cache_for_users():
    invalidate_cache_by_prefix("cache:/api/admin/users")

def invalidate_user_profile_cache(user_id=None):
    if user_id is None:
        raise ValueError("user_id is required")
    invalidate_cache_by_prefix(f"cache:/api/user/profile:user:{user_id}")


def rate_limit(limit=100, window=60):   # 10 requests per minute
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            redis = get_redis()
            ip = request.remote_addr
            key = f"rate_limit:{ip}:{request.endpoint}"
            current = redis.get(key)
            if current:
                current = int(current)
                if current >= limit:
                    return {"msg": "Rate limit exceeded. Try again later."}, 429
                else:
                    redis.incr(key)
            else:
                redis.setex(key, window, 1)
            return func(*args, **kwargs)
        return wrapper
    return decorator