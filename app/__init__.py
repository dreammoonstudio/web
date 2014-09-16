from flask import Flask
from flask import flash as f
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from config import config

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
babel = Babel()
pagedown = PageDown()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	babel.init_app(app)
	login_manager.init_app(app)
	pagedown.init_app(app)

	from app.main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

# global functions
def flash(message="", flag=False):
	if flag:
		f(flag + '/' + message);
	else:
		f(message);
