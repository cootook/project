import os

from datetime import timedelta

class Config(object):
    """Base config class containing all environment variables and hardcoded values."""
    
    # Flask Core Settings
    SECRET_KEY = os.environ.get("SECRET_KEY",)
    STATIC_FOLDER = os.environ.get("FLASK_STATIC_FOLDER")
    TEMPLATE_FOLDER = os.environ.get("FLASK_TEMPLATE_FOLDER")
    TEMPLATES_AUTO_RELOAD = True

    # Session Configuration
    SESSION_PERMANENT = True
    SESSION_TYPE = os.environ.get('FLASK_SESSION_TYPE')
    SESSION_FILE_THRESHOLD = int(os.environ.get('FLASK_SESSION_FILE_THRESHOLD'))
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.environ.get('FLASK_SESSION_LIFETIME_DAYS')))
    
    # Security Settings
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_USERNAME_ENABLE = False
    # SECURITY_CSRF_PROTECT_MECHANISMS = ['session', 'basic']
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = False
    
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
    DATA_CALLBACK_JS_FUNC_NAME = "set_is_recaptcha_true"
    DATA_EXPIRED_CALLBACK_JS_FUNC_NAME = "set_is_recaptcha_false"

    # Flask WTF recaptcha
    RECAPTCHA_PUBLIC_KEY = SITE_KEY_RECAPTCHA
    RECAPTCHA_PRIVATE_KEY = SECRET_RECAPTCHA
    RECAPTCHA_DATA_ATTRS = {
        "callback": DATA_CALLBACK_JS_FUNC_NAME, 
        "expired-callback": DATA_EXPIRED_CALLBACK_JS_FUNC_NAME
    }

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