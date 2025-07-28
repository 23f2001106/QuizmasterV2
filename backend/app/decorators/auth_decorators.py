from functools import wraps
from flask import jsonify, g, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.query.get(identity)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        if not user.is_admin():
            return jsonify({"msg": "Admin access required"}), 403

        if not user.is_active():
            return jsonify({"msg": "Account is suspended"}), 403
        
        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper

def get_current_user_or_abort(require_verified=False):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        abort(404, message="User not found")
    if not user.is_active():
        abort(403, message="Account is suspended")
    if require_verified and not user.is_verified:
        abort(403, message="Account not verified. Please verify your email.")
    return user

def verified_and_active_user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        get_current_user_or_abort(require_verified=True)
        return fn(*args, **kwargs)
    return wrapper
