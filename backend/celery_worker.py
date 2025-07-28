from app import create_app, create_celery

app = create_app()
celery = create_celery(app)

if __name__ == '__main__':
    # This script is used to start a worker manually
    # Command: celery -A celery_worker.celery worker --loglevel=info
    celery.start()