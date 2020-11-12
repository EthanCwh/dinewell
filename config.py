import os
import config

class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get(
        'SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///dwdb.db'

    MAILGUN_API = os.environ.get(
        'MAILGUN_API')

    HERE_API = os.environ.get(
        'HERE_API')

    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False

