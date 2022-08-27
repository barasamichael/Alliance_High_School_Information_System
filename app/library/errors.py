import flask
from . import library

@library.app_errorhandler(403)
def forbidden(e):
    return flask.render_template('library/403.html'), 403


@library.app_errorhandler(404)
def page_not_found(e):
    return flask.render_template('library/404.html'), 404


@library.app_errorhandler(500)
def internal_server_error(e):
    return flask.render_template('library/500.html'), 500
