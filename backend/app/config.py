from dotenv import load_dotenv
import os
from datetime import timedelta
from celery.schedules import crontab

load_dotenv()

class Config:
    DEBUG = True
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')

    CORS_ORIGINS = ["http://localhost:8080"]
    BASE_URL = 'http://localhost:8080'

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///quizmaster.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_HEADER_NAME = 'Authorization' 
    JWT_HEADER_TYPE = 'Bearer'

    # Flask-Caching (using Redis)
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 1  # Separate Redis DB for cache if preferred
    CACHE_DEFAULT_TIMEOUT = 300

    # SMTP Config 
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 1025))
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')
    
    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
    CELERY_TIMEZONE = 'Asia/Kolkata'
    CELERY_ENABLE_UTC = False

    # Celery Beat schedule
    CELERY_BEAT_SCHEDULE = {
        'cleanup-unverified-users-daily': {
            'task': 'delete_unverified_users_older_than',
            'schedule': crontab(minute=0, hour=3),  # Every day at 3 AM
            'args': (24,)
        },
        'send-daily-reminders': {
            'task': 'send_daily_reminders',
            'schedule': crontab(minute=0, hour='6-23'),  # Every hour from 6AM to 11PM
        },
        'send-monthly-report': {
            'task': 'send_monthly_report',
            'schedule': crontab(minute=0, hour=6, day_of_month='28-31'),  # End of each month
            'options': {'expires': 86400}  # expire task after 1 day
        },
    }
