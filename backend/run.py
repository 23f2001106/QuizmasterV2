from app import create_app, create_celery
from app.api import register_api

app = create_app()
celery = create_celery(app)
register_api(app)

if __name__ == '__main__':
    app.run(debug=True)




