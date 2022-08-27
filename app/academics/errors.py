from flask import render_template
from . import academics


@academics.app_errorhandler(403)
def forbidden(e):
    return render_template('academics/403.html'), 403


@academics.app_errorhandler(404)
def page_not_found(e):
    return render_template('academics/404.html'), 404


@academics.app_errorhandler(500)
def internal_server_error(e):
    return render_template('academics/500.html'), 500
