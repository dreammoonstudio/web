import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECCRET_KEY') or 'this-is-a-temporary-secret-key'
	
	# SQLAlchemy
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True

	# mail
	DM_MAIL_SUBJECT_PREFIX = '[Dream Moon Studio]'
	DM_MAIL_SENDER = 'Dream Moon Admin <admin@dreammoonstudio.com>'
	DM_ADMIN = os.environ.get('DM_ADMIN')

	MAIL_SERVER_OUT = "smtpout.secureserver.net"
	MAIL_SERVER_IN = "pop.secureserver.net"
	MAIL_PORT = 465
	MAIL_USERNAME = os.environ.get('DM_MAIL_USERNAME')
	MAIL_USERNAME = os.environ.get('DM_MAIL_PASSWORD')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')

config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'deploy': ProductionConfig,
    'default': DevelopmentConfig
}

LANGUAGES = {
	'en' : 'English',
	'zh' : 'Chinese'
}
