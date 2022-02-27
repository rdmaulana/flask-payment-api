import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from celery import Celery

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

cors = CORS()

bcrypt = Bcrypt()

mongo = PyMongo()

jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder=None)

    app_settings = os.getenv(
        'APP_SETTINGS',
        'app.config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)
    app.json_encoder = JSONEncoder

    initialize_extensions(app)
    register_blueprints(app)

    return app

def initialize_extensions(app):
    cors.init_app(app)
    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    # celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    # celery.conf.update(app.config)

# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery

def register_blueprints(app):
    from app.views import route_not_found, method_not_found, internal_server_error, bad_request
    from app.controllers import user, transaction, profile

    app.register_blueprint(
        user.auth,
        url_prefix='/api/v1/auth/'
    )

    app.register_blueprint(
        transaction.transaction,
        url_prefix='/api/v1/transaction/'
    )

    app.register_blueprint(
        profile.profile,
        url_prefix='/api/v1/profile/'
    )

    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, route_not_found)
    app.register_error_handler(405, method_not_found)
    app.register_error_handler(500, internal_server_error)

