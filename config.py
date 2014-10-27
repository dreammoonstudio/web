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
    DM_ADMIN = "Dream Moon Admin"

    MAIL_SERVER = config.get('DM', 'EMAIL_SERVER')
    MAIL_PORT = config.get('DM', 'EMAIL_PORT')
    MAIL_USERNAME = config.get('DM', 'EMAIL_USERNAME')
    MAIL_PASSWORD = config.get('DM', 'EMAIL_PASSWORD')

    MAIL_USE_SSL = True

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
