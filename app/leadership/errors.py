from flask import render_template
from . import leadership


@leadership.app_errorhandler(403)
def forbidden(e):
    return render_template('leadership/403.html'), 403


@leadership.app_errorhandler(404)
def page_not_found(e):
    return render_template('leadership/404.html'), 404


@leadership.app_errorhandler(500)
def internal_server_error(e):
    return render_template('leadership/500.html'), 500


@leadership.app_errorhandler(400)
def invalid_image(e):
    return render_template('leadership/400.html'), 400
