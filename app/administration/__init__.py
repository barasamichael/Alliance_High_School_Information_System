from flask import Blueprint, current_app
administration = Blueprint('administration', __name__)
from . import views, errors

@administration.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
