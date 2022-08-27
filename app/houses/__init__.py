from flask import Blueprint, current_app
houses = Blueprint('houses', __name__)
from . import views, errors

@houses.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
