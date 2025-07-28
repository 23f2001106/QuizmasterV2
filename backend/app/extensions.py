from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from redis import Redis
from celery import Celery
from flask import current_app

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()  
migrate = Migrate()
cache = Cache() 

celery: Celery = None


def get_mail_config():
    return {
        "MAIL_SERVER": current_app.config['MAIL_SERVER'],
        "MAIL_PORT": current_app.config['MAIL_PORT'],
        "MAIL_USERNAME": current_app.config['MAIL_USERNAME'],
        "MAIL_PASSWORD": current_app.config['MAIL_PASSWORD'],
        "MAIL_USE_TLS": current_app.config['MAIL_USE_TLS'],
        "MAIL_USE_SSL": current_app.config['MAIL_USE_SSL'],
        "MAIL_DEFAULT_SENDER": current_app.config['MAIL_DEFAULT_SENDER'],
    }