import os
import configparser

config = configparser.RawConfigParser()
config.read("setting.cfg")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = config.get('DM', 'SECRET_KEY')
    
    # SQLAlchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # mail
    DM_MAIL_SUBJECT_PREFIX = '[Dream Moon Studio]'
    DM_MAIL_SENDER = 'Dream Moon Admin <admin@dreammoonstudio.com>'
    DM_ADMIN = 'admin@dreammoonstudio.com'
    CREATOR_EMAIL = config.get('DM', 'CREATOR_EMAIL')

    MAIL_SERVER = config.get('DM', 'EMAIL_SERVER')
    MAIL_PORT = config.get('DM', 'EMAIL_PORT')
    MAIL_USERNAME = config.get('DM', 'EMAIL_USERNAME')
    MAIL_PASSWORD = config.get('DM', 'EMAIL_PASSWORD')

    MAIL_USE_SSL = True

    # debug
    SQLALCHEMY_RECORD_QUERIES = True
    SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = config.get('DM', 'DATABASE_URI')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to admin
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.DM_MAIL_SENDER,
            toaddrs=[cls.DM_ADMIN, cls.CREATOR_EMAIL],
            subject=cls.DM_MAIL_SUBJECT_PREFIX + " Application Error",
            credentials=credentials,
            secure=secure
            )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class AlphaTestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'alpha-test.sqlite')

config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'deploy': ProductionConfig,
    'default': DevelopmentConfig,
    'alpha': AlphaTestConfig
}

LANGUAGES = {
    'en' : 'English',
    'zh' : 'Chinese'
}
