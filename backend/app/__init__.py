from flask import Flask
from redis import Redis
from celery import Celery
from flask import jsonify

from .extensions import db, jwt, cors, migrate, cache
from .celery_app import init_celery       
from .tasks import *
from .utils.init_admin import initialize_admin


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Invalid token: {error}")
        return jsonify({"msg": "Invalid token"}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print("Expired token")
        return jsonify({"msg": "Token expired"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"Missing token: {error}")
        return jsonify({"msg": "Missing Authorization Header"}), 401

    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    migrate.init_app(app, db)
    cache.init_app(app)

    redis_instance = Redis(
        host=app.config.get('REDIS_HOST', 'localhost'),
        port=app.config.get('REDIS_PORT', 6379),
        db=app.config.get('REDIS_DB', 0),
        decode_responses=True  
    )

    app.redis_client = redis_instance

    with app.app_context():
        initialize_admin()

    return app


def create_celery(app):
    
    celery_instance = Celery(app.import_name)
    celery_instance.config_from_object(app.config, namespace='CELERY')

    init_celery(celery_instance, app)

    celery_instance.conf.beat_schedule = app.config.get('CELERY_BEAT_SCHEDULE', {})
    celery_instance.conf.timezone =  app.config.get('CELERY_TIMEZONE', 'Asia/Kolkata')
    celery_instance.conf.enable_utc = False

    register_email_tasks(celery_instance)
    register_cleanup_tasks(celery_instance)
    register_report_tasks(celery_instance)
    register_reminder_tasks(celery_instance)
    register_export_tasks(celery_instance)

    app.celery = celery_instance 
      
    return celery_instance
