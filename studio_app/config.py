import os

from datetime import timedelta

class Config(object):
    # """Base config."""

    # SECRET_RECAPTCHA = os.environ.get("SECRET_RECAPTCHA")
    # URL_RECAPTCHA = os.environ.get("URL_RECAPTCHA")

    # SECRET_KEY = os.environ.get("SECRET_KEY")
    # SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    # TEMPLATES_AUTO_RELOAD = True

    # SESSION_PERMANENT = True
    # SESSION_TYPE = os.environ.get('FLASK_SESSION_TYPE')
    # SESSION_FILE_THRESHOLD = int(os.environ.get('FLASK_SESSION_FILE_THRESHOLD'))
    # PERMANENT_SESSION_LIFETIME = timedelta(days = int(os.environ.get('FLASK_SESSION_LIFETIME_DAYS')))
    
    # SECURITY_CONFIRMABLE = False
    # SECURITY_RECOVERABLE = True
    # SECURITY_REGISTERABLE = True
    # SECURITY_TRACKABLE = True
    # SECURITY_USERNAME_ENABLE = False
    
    # MAIL_SERVER = os.getenv("MAIL_SERVER")
    # MAIL_PORT = os.getenv("MAIL_PORT")

    # MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    # MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    # MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    # MAIL_DEFAULT_SENDER_NAME = os.getenv("MAIL_DEFAULT_SENDER_NAME")
    # MAIL_DEFAULT_DOMAIN = os.getenv("MAIL_DEFAULT_DOMAIN")

    # DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")

    # TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")
    # TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID")
    # TWILIO_FROM_NUMBER=os.getenv("TWILIO_FROM_NUMBER")
    # TWILIO_SITE_LINK=os.getenv("TWILIO_SITE_LINK")
    # TWILIO_BUSINESS_NAME=os.getenv("TWILIO_BUSINESS_NAME")
    # TWILIO_SMS_HEADER=os.getenv("TWILIO_BUSINESS_NAME")
    # TWILIO_SMS_FOOTER=os.getenv("TWILIO_BUSINESS_NAME")

    # # flask-sqlalchemy
    #     # As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
    # # underlying engine. This option makes sure that DB connections from the
    # # pool are still valid. Important for entire application since
    # # many DBaaS options automatically close idle connections.


    # # flask/flask_login
    # REMEMBER_COOKIE_SAMESITE = os.environ.get("FLASK_LOGIN_REMEMBER_COOKIE_SAMESITE")
    # SESSION_COOKIE_SAMESITE = os.environ.get("FLASK_LOGIN_SESSION_COOKIE_SAMESITE")   


    # MAIL_USE_SSL = False
    # MAIL_USE_TLS = True

    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     "pool_pre_ping": True,
    # }
    # SQLALCHEMY_TRACK_MODIFICATIONS = False 

    """Base config class containing all environment variables and hardcoded values."""
    
    # Flask Core Settings
    SECRET_KEY = os.environ.get("SECRET_KEY",)
    STATIC_FOLDER = os.environ.get("FLASK_STATIC_FOLDER", "../studio_app/static/")
    TEMPLATE_FOLDER = os.environ.get("FLASK_TEMPLATE_FOLDER", "../studio_app/templates/")
    TEMPLATES_AUTO_RELOAD = True

    # Session Configuration
    SESSION_PERMANENT = True
    SESSION_TYPE = os.environ.get('FLASK_SESSION_TYPE', 'filesystem')
    SESSION_FILE_THRESHOLD = int(os.environ.get('FLASK_SESSION_FILE_THRESHOLD', '250'))
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.environ.get('FLASK_SESSION_LIFETIME_DAYS', '90')))
    
    # Security Settings
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_USERNAME_ENABLE = False
    
    # Cookie Settings
    REMEMBER_COOKIE_SAMESITE = os.environ.get("FLASK_LOGIN_REMEMBER_COOKIE_SAMESITE", "strict")
    SESSION_COOKIE_SAMESITE = os.environ.get("FLASK_LOGIN_SESSION_COOKIE_SAMESITE", "strict")

    # Email Configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT"))
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_DEFAULT_SENDER_NAME = os.environ.get("MAIL_DEFAULT_SENDER_NAME")
    MAIL_DEFAULT_DOMAIN = os.environ.get("MAIL_DEFAULT_DOMAIN")

    # Google reCAPTCHA Settings
    SECRET_RECAPTCHA = os.environ.get("SECRET_RECAPTCHA")
    SITE_KEY_RECAPTCHA = os.environ.get("SITE_KEY_RECAPTCHA")
    URL_RECAPTCHA = os.environ.get("URL_RECAPTCHA")

    # User Role Settings
    KEY_CHANGE_ROLE_LIST = os.environ.get("KEY_CHANGE_ROLE_LIST")
    KEY_CHANGE_ROLE = os.environ.get("KEY_CHANGE_ROLE")

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///db_v2.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    # Business Hours Configuration
    OPEN_AT_TIME_HOUR = int(os.environ.get("OPEN_AT_TIME_HOUR"))
    OPEN_AT_TIME_MINUTE = int(os.environ.get("OPEN_AT_TIME_MINUTE"))
    CLOSE_AT_TIME_HOUR = int(os.environ.get("CLOSE_AT_TIME_HOUR"))
    CLOSE_AT_TIME_MINUTE = int(os.environ.get("CLOSE_AT_TIME_MINUTE"))
    TIME_DELTA_SLOTS_MINUTES = int(os.environ.get("TIME_DELTA_SLOTS_MINUTES"))
    HOW_FAR_IN_FUTURE_CREATE_SLOTS = int(os.environ.get("HOW_FAR_IN_FUTURE_CREATE_SLOTS"))

    # Twilio Configuration
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
    TWILIO_SITE_LINK = os.environ.get("TWILIO_SITE_LINK")
    TWILIO_BUSINESS_NAME = os.environ.get("TWILIO_BUSINESS_NAME")
    TWILIO_SMS_HEADER = os.environ.get("TWILIO_SMS_HEADER")
    TWILIO_SMS_FOOTER = os.environ.get("TWILIO_SMS_FOOTER")

    # Administrator Settings
    ADMINISTRATOR_EMAIL = os.environ.get("ADMINISTRATOR_EMAIL")
    ADMINISTRATOR_PASSWORD = os.environ.get("ADMINISTRATOR_PASSWORD")
    ADMINISTRATOR_NAME = os.environ.get("ADMINISTRATOR_NAME")
    ADMINISTRATOR_US_PHONE = os.environ.get("ADMINISTRATOR_US_PHONE")

    # Test User Settings
    TEST_USER_EMAIL = os.environ.get("TEST_USER_EMAIL")
    TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD")
    TEST_USER_NAME = os.environ.get("TEST_USER_NAME")
    TEST_USER_US_PHONE = os.environ.get("TEST_USER_US_PHONE")

    # Default User Settings
    DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")



class ProductionConfig(Config):
    """Uses production database server."""
    TESTING = False
    FLASK_ENV = 'production'
    FLASK_DEBUG = False 

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class DevelopmentConfig(Config):
    TESTING = False

    FLASK_ENV='development'
    FLASK_DEBUG=True

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class TestingConfig(Config):
    TESTING = True

    FLASK_ENV = 'production'
    FLASK_DEBUG = False 

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'