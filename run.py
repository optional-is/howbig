# coding: utf-8

import logging
import flask
import json
import flask_config
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

# See http://blog.y3xz.com/blog/2012/08/16/flask-and-postgresql-on-heroku/ for how to use postgres on Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

app.static_folder = "templates"
app.SEND_FILE_MAX_AGE_DEFAULT = 0


@app.route('/examples')
def examples():
	"""Returns static html"""

	return file('templates/example.html').read()


@app.route('/dimension/<shape_file>')
def dimension():
	"""Returns a details page about the shape file"""

	return file('templates/detail.html').read()

@app.route('/category/<tag>')
def dimension():
	"""Returns a list page of all the shape files that match the category"""

	return file('templates/list.html').read()

@app.route('/category')
def dimension():
	"""Returns a list page of all the categories/tags"""

	return file('templates/list.html').read()


@app.route('/')
def home():
	"""Returns html with an overview of shapes to compare the sizes-of """


	return file('templates/index.html').read()


if __name__ == '__main__':
	# Set up logging to stdout, which ends up in Heroku logs
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.WARNING)
	app.logger.addHandler(stream_handler)

	app.debug = False
	app.run(host='0.0.0.0', port=flask_config.port)
