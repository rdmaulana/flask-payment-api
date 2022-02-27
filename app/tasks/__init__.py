import os

from celery import Celery
from app import create_app

flask_app = create_app()

celery = Celery(__name__)
celery.conf.broker_url = flask_app.config["CELERY_BROKER_URL"]
celery.conf.result_backend = flask_app.config["CELERY_RESULT_BACKEND"]
celery.conf.include=['app.tasks.transfer']