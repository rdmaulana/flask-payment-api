import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dotenv_path = join(dirname(__file__), './../.env')
load_dotenv(dotenv_path)

class BaseConfig(object):
    DEBUG = False
    JWT_SECRET_KEY = os.environ['SECRET_KEY']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    MONGO_URI = os.environ['DATABASE_URL']
    REDISTOGO_URL = os.environ['REDIS_URL']
    CSRF_ENABLED = True
    BCRYPT_HASH_PREFIX = 14
    BCRYPT_LOG_ROUNDS = 12
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000

class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BCRYPT_HASH_PREFIX = 4
    AUTH_TOKEN_EXPIRY_DAYS = 0
    AUTH_TOKEN_EXPIRY_SECONDS = 3
    AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS = 5

class ProductionConfig(BaseConfig):
    DEBUG = False
