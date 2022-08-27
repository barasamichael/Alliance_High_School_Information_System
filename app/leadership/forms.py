from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Length, Regexp, DataRequired, Email

from ..models import (student)


class UpdateProfileImageForm(FlaskForm):
    file = FileField('select image file', validators = [FileRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Select image files only.')])
    submit = SubmitField('submit')
