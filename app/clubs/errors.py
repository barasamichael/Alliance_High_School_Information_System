from flask import render_template
from . import clubs

@clubs.app_errorhandler(403)
def forbidden(e):
    return render_template('clubs/403.html'), 403


@clubs.app_errorhandler(404)
def page_not_found(e):
    return render_template('clubs/404.html'), 404


@clubs.app_errorhandler(500)
def internal_server_error(e):
    return render_template('clubs/500.html'), 500
