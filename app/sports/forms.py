from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Length, Regexp, DataRequired, Email

from ..models import (student, sport, sport_notification, sport_team, 
        sport_position, sport_event, sport_coach, sport_assignment, school)


class UpdateSportProfileImageForm(FlaskForm):
    file = FileField('select image file', validators = [FileRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Select image files only.')])
    submit = SubmitField('submit')


class RegisterSchoolForm(FlaskForm):
    title = StringField('school name', validators = [DataRequired(), 
        Length(1, 255)])
    nickname = StringField('nickname', validators = [DataRequired(), 
        Length(1, 128)])
    submit = SubmitField('submit')


class RegisterCoachForm(FlaskForm):
    first_name = StringField('first name', 
            validators = [DataRequired(), Length(1, 64)])
    middle_name = StringField('middle name', validators = [Length(1, 64)])
    last_name = StringField('last name', validators = [Length(1, 64)])

    email_address = StringField('email address', 
            validators = [DataRequired(), Length(1, 128), Email()])
    phone_no = StringField('phone number', 
            validators = [DataRequired(), Length(1, 32)])
    residential_address = StringField('residential address', 
            validators = [DataRequired(), Length(1, 128)])

    year_appointed = StringField('year appointed', 
            validators = [DataRequired(), Length(1, 8)])

    submit = SubmitField('submit')


class RegisterTeamForm(FlaskForm):
    team_name = StringField('enter team name', 
            validators = [DataRequired(), Length(1, 128)])
    submit = SubmitField('submit')


class RegisterSportForm(FlaskForm):
    sport_name = StringField('enter name of sport', validators = 
            [DataRequired(), Length(1, 128)])
    year_established = StringField('enter year established', validators = 
            [DataRequired(), Length(1, 8)])

    submit = SubmitField('submit')


class RegisterPositionForm(FlaskForm):
    submit = SubmitField('submit')


class RegisterNotificationForm(FlaskForm):
    submit = SubmitField('submit')


class RegisterEventForm(FlaskForm):
    submit = SubmitField('submit')


class SportAssignmentForm(FlaskForm):
    submit = SubmitField('submit')
