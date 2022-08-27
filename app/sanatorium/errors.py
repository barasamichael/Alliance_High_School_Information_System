from flask import render_template
from . import sanatorium


@sanatorium.app_errorhandler(403)
def forbidden(e):
    return render_template('sanatorium/403.html'), 403


@sanatorium.app_errorhandler(404)
def page_not_found(e):
    return render_template('sanatorium/404.html'), 404


@sanatorium.app_errorhandler(500)
def internal_server_error(e):
    return render_template('sanatorium/500.html'), 500
