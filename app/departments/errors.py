from flask import render_template
from . import departments


@departments.app_errorhandler(403)
def forbidden(e):
    return render_template('departments/403.html'), 403


@departments.app_errorhandler(404)
def page_not_found(e):
    return render_template('departments/404.html'), 404


@departments.app_errorhandler(500)
def internal_server_error(e):
    return render_template('departments/500.html'), 500
