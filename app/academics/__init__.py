from flask import Blueprint, current_app
academics = Blueprint('academics', __name__)
from . import views, errors

@academics.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
