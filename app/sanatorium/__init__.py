from flask import Blueprint, current_app
sanatorium = Blueprint('sanatorium', __name__)
from . import views, errors

@sanatorium.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
