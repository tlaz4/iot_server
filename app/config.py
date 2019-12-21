import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	'''
	Base config class
	'''

	Debug = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
