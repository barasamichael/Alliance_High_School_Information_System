from flask import Blueprint, current_app
leadership = Blueprint('leadership', __name__)
from . import views, errors

@leadership.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
