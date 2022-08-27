from flask import Blueprint, current_app
clubs = Blueprint('clubs', __name__)
from . import views, errors

@clubs.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
