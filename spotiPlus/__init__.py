import os

from flask import Flask

def create_app(test_config=None):
	#create and configure the app
	app = Flask(__name__, instance_relative_config=True)

	#default config that the app will use.
	app.config.from_mapping(
		#should be overriten during deployment, 'dev' is convinient for now.
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'spotiPlus.sqlite'), 
	)

	#overrides default config with values taken from 'config.py'
	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	
	else:
		app.config.from_mapping(test_config)

	#ensure that 'app.instance_path' exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import spotiplus
	app.register_blueprint(spotiplus.bp)

	return app














