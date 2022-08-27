from flask import Blueprint, current_app
obc = Blueprint('obc', __name__)
from . import views, errors

@obc.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
