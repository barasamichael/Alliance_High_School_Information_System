from flask import Blueprint, current_app
sports = Blueprint('sports', __name__)
from . import views, errors

@sports.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
