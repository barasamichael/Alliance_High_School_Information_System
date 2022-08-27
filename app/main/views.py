import flask
from . import main
from .. import db


@main.route('/')
@main.route('/home')
@main.route('/homepage')
def homepage():
    return flask.render_template('main/homepage.html')

@main.route('/about_us')
def about_us():
    return flask.render_template('main/about_us.html')
