from flask import render_template
from . import students


@students.app_errorhandler(403)
def forbidden(e):
    return render_template('students/403.html'), 403


@students.app_errorhandler(404)
def page_not_found(e):
    return render_template('students/404.html'), 404


@students.app_errorhandler(500)
def internal_server_error(e):
    return render_template('students/500.html'), 500
