from flask import render_template
from . import obc


@obc.app_errorhandler(403)
def forbidden(e):
    return render_template('obc/403.html'), 403


@obc.app_errorhandler(404)
def page_not_found(e):
    return render_template('obc/404.html'), 404


@obc.app_errorhandler(500)
def internal_server_error(e):
    return render_template('obc/500.html'), 500
