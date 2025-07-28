from app import create_app, create_celery

app = create_app()
celery = create_celery(app)

if __name__ == '__main__':
    # This script runs Celery beat (the scheduler)
    # Command: celery -A celery_beat.celery beat --loglevel=info
    celery.start(argv=['celery', 'beat'])
