import flask

library = flask.Blueprint('library', __name__)

from . import views, forms, errors

@library.app_errorhandler
def global_variables():
    return dict(app_name = flask.current_app.config['ORGANISATION_NAME'])
