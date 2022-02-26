import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from rq import Queue
from rq.job import Job
from worker import conn

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

app = Flask(__name__, static_folder=None)

CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)

mongo = PyMongo(app)

jwt = JWTManager(app)
app.json_encoder = JSONEncoder

q = Queue(connection=conn)

from app import views

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