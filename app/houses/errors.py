from flask import render_template
from . import houses

@houses.app_errorhandler(403)
def forbidden(e):
    return render_template('houses/403.html'), 403


@houses.app_errorhandler(404)
def page_not_found(e):
    return render_template('houses/404.html'), 404


@houses.app_errorhandler(500)
def internal_server_error(e):
    return render_template('houses/500.html'), 500
