from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextField, SubmitField, SelectField, FileField
from wtforms import ValidationError
from wtforms.validators import Length, Regexp, DataRequired, Email
from wtforms.fields.html5 import DateField, TimeField
from ..models import club


class RegisterClubScheduleForm(FlaskForm):
    day = SelectField('select day', choices = [('Monday','Monday'),
        ('Tuesday','Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday','Thursday'), 
        ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')],
        validators = [DataRequired(), Length(1, 32)])

    description = StringField('description', 
            validators = [DataRequired(), Length(1, 255)])
    start_time = TimeField('start time', validators = [DataRequired()])
    end_time = TimeField('end time', validators = [DataRequired()])
    submit = SubmitField('submit')


class RegisterSpeakerForm(FlaskForm):
    first_name = StringField('first name', 
            validators = [DataRequired(), Length(1, 64)])
    last_name = StringField('last name', 
            validators = [DataRequired(), Length(1, 64)])
    gender = SelectField('gender', choices = [('male','male'),('female','female')], 
            validators = [DataRequired(), Length(1, 32)])
    email_address = StringField('email address', 
            validators = [DataRequired(), Length(1, 64), Email()])
    profession = StringField('profession', 
            validators = [DataRequired(), Length(1, 128)])

    submit = SubmitField('submit')


class ClubWallPaperForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(), 
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Select Image Files Only.')])

    submit = SubmitField('submit')


class ClubEventWallPaperForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Select Image Files Only.')])

    submit = SubmitField('submit')



class EventRegistrationForm(FlaskForm):
    title = StringField('event title', 
            validators = [DataRequired(), Length(1, 128)])
    date_scheduled = DateField('date scheduled', validators = [DataRequired()])
    description = TextField('brief description', validators = [DataRequired()])

    start_time = TimeField('from', validators = [DataRequired()])
    end_time = TimeField('to', validators = [DataRequired()])
    venue = StringField('venue', validators = [DataRequired(), Length(1, 128)])

    submit = SubmitField('submit')


class AchievementRegistrationForm(FlaskForm):
    description = StringField('description', 
            validators = [DataRequired(), Length(1, 255)])
    
    year_achieved = StringField('year achieved', 
            validators = [DataRequired(), Length(1, 32)])

    submit = SubmitField('submit')


class FounderRegistrationForm(FlaskForm):
    names = StringField('names', validators = [DataRequired(), Length(1, 128)])
    gender = SelectField('gender', choices = [('male', 'male'),('female','female')],
            validators = [DataRequired()])
    email_address = StringField('email address', validators = [Length(1, 128), 
        Email(), 
        Regexp('^[A-Za-z][A-Za-z]',0,'Non-alphabetical characters not allowed.')]
        )
    submit = SubmitField('submit')


class ClubRegistrationForm(FlaskForm):
    club_name = StringField('club name', 
        validators = [DataRequired(), Length(1, 64), 
        Regexp('^[A-Za-z][A-Za-z]',0,'Non-alphabetical characters not allowed.')])

    year_founded = StringField('year founded', validators = 
            [DataRequired(), Length(1, 32)])

    venue = StringField('venue', validators = [DataRequired(), Length(1, 64)])
    mission = StringField('mission', validators = [DataRequired(), Length(1, 255)])
    vision = TextField('vision', validators = [DataRequired(), Length(1, 255)])

    email_address = StringField('email address', 
            validators = [DataRequired(), Length(1, 128), Email()])

    about_us = TextField('about us', validators = [DataRequired()])

    submit = SubmitField('submit')

    def validate_club_name(self, field):
        if club.query.filter_by(club_name = field.data).first():
            raise ValidationError('Club already registered!!!')

    def validate_email_address(self, field):
        if club.query.filter_by(email_address = field.data).first():
            raise ValidationError('Email address already in use.')

    def validate_venue(self, field):
        if club.query.filter_by(venue = field.data).first():
            raise ValidationError('Venue already in use.')
