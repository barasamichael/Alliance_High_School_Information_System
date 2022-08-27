from flask import Blueprint, current_app
students = Blueprint('students', __name__)
from . import views, errors

@students.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
