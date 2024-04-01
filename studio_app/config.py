import os

from datetime import timedelta

class Config(object):
    """Base config."""
    TESTING = False
    FLASK_ENV = 'production'
    FLASK_DEBUG = False 

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    # Configure session to use filesystem (instead of signed cookies)
    SESSION_PERMANENT = True
    SESSION_TYPE = os.environ.get('FLASK_SESSION_TYPE')
    SESSION_FILE_THRESHOLD = int(os.environ.get('FLASK_SESSION_FILE_THRESHOLD'))
    PERMANENT_SESSION_LIFETIME = timedelta(days = int(os.environ.get('FLASK_SESSION_LIFETIME_DAYS')))

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    # MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_APP_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # flask-sqlalchemy
        # As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
    # underlying engine. This option makes sure that DB connections from the
    # pool are still valid. Important for entire application since
    # many DBaaS options automatically close idle connections.
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask/flask_login
    REMEMBER_COOKIE_SAMESITE = os.environ.get("FLASK_LOGIN_REMEMBER_COOKIE_SAMESITE")
    SESSION_COOKIE_SAMESITE = os.environ.get("FLASK_LOGIN_SESSION_COOKIE_SAMESITE")    

class ProductionConfig(Config):
    """Uses production database server."""
    FLASK_ENV = 'production'
    FLASK_DEBUG = False 

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class DevelopmentConfig(Config):
    FLASK_ENV='development'
    FLASK_DEBUG=True

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class TestingConfig(Config):
    TESTING = True

    FLASK_ENV = 'production'
    FLASK_DEBUG = False 

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'