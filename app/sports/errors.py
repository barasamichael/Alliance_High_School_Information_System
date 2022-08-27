from flask import render_template
from . import sports


@sports.app_errorhandler(403)
def forbidden(e):
    return render_template('sports/403.html'), 403


@sports.app_errorhandler(404)
def page_not_found(e):
    return render_template('sports/404.html'), 404


@sports.app_errorhandler(500)
def internal_server_error(e):
    return render_template('sports/500.html'), 500


@sports.app_errorhandler(400)
def invalid_image(e):
    return render_template('sports/400.html'), 400
