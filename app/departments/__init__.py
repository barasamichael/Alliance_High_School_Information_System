from flask import Blueprint, current_app
departments = Blueprint('departments', __name__)
from . import views, errors

@departments.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
