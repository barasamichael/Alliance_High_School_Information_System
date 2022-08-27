from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField, FileField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.fields.html5 import DateField, TimeField

from ..models import obc_event, obc


class UpdateOBCForm(FlaskForm):
    admission_no = IntegerField('admission number', validators = [DataRequired()])
    first_name = StringField('first name',
            validators = [DataRequired(), Length(1, 64)])
    middle_name = StringField('middle name',
            validators = [DataRequired(), Length(1, 64)])
    last_name = StringField('last name',
            validators = [DataRequired(), Length(1, 64)])

    gender = SelectField('gender', choices = [('male','male'),('female','female')],
            validators = [DataRequired(), Length(1, 32)])

    date_of_birth = DateField('date of birth', validators = [DataRequired()])

    email_address = StringField('email address',
            validators = [DataRequired(), Length(1, 128), Email()])

    phone_no = StringField('phone number',
            validators = [DataRequired(), Length(1, 64)])

    residential_address = StringField('residential address',
            validators = [DataRequired(), Length(1, 255)])

    profession = StringField('profession',
            validators = [DataRequired(), Length(1, 255)])

    year = StringField('year of ...', validators = [DataRequired(), Length(1, 16)])

    house_id = SelectField('house', validators = [DataRequired(), Length(1, 64)])

    status = SelectField('status', choices = [
        ('Chairman', 'Chairman'), ('Vice Chairman', 'Vice Chairman'), 
        ('Secretary', 'Secretary'), ('Assistant Secretary', 'Assistant Secretary'), 
        ('Treasurer', 'Treasurer'), ('Assistant Treasurer', 'Assistant Treasurer'),
        ('Committee Member', 'Committee Member'), ('member', 'member')], 
        validators = [DataRequired(), Length(1, 128)])

    submit = SubmitField('submit')

class ObcProfileImageForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Select Image Files Only.')])

    submit = SubmitField('submit')


class RegisterObcEventForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 128)])
    description = StringField('description', 
            validators = [DataRequired(), Length(1, 1024)])
    date_scheduled = DateField('date scheduled', validators = [DataRequired()])
    venue = StringField('venue', validators = [DataRequired(), Length(1, 128)])
    start_time = TimeField('start time', validators = [DataRequired()])
    end_time = TimeField('end time', validators = [DataRequired()])

    submit = SubmitField('submit')

    def validate_title(self, field):
        if obc_event.query.filter_by(title= field.data).first():
            raise ValidationError('event already registered.')


class RegisterOBCForm(FlaskForm):
    admission_no = IntegerField('admission number', validators = [DataRequired()])
    first_name = StringField('first name', 
            validators = [DataRequired(), Length(1, 64)])
    middle_name = StringField('middle name', 
            validators = [DataRequired(), Length(1, 64)])
    last_name = StringField('last name', 
            validators = [DataRequired(), Length(1, 64)])

    gender = SelectField('gender', choices = [('male','male'),('female','female')], 
            validators = [DataRequired(), Length(1, 32)])

    date_of_birth = DateField('date of birth', validators = [DataRequired()])

    email_address = StringField('email address', 
            validators = [DataRequired(), Length(1, 128), Email()])

    phone_no = StringField('phone number', 
            validators = [DataRequired(), Length(1, 64)])

    residential_address = StringField('residential address', 
            validators = [DataRequired(), Length(1, 255)])

    profession = StringField('profession', 
            validators = [DataRequired(), Length(1, 255)])

    year = StringField('year of ...', validators = [DataRequired(), Length(1, 16)])

    house_id = SelectField('house', validators = [DataRequired(), Length(1, 64)])

    submit = SubmitField('submit')

    def validate_admission_no(self, field):
        if obc.query.filter_by(adm_no= field.data).first():
            raise ValidationError('member already exists.')

    def validate_phone_no(self, field):
        if obc.query.filter_by(phone_no = field.data).first():
            raise ValidationError('phone number already exists.')

    def validate_email_address(self, field):
        if obc.query.filter_by(email_address = field.data).first():
            raise ValidationError('email address already exists.')


class ObcAchievementForm(FlaskForm):
    description = StringField('description of achievement', 
            validators = [DataRequired(), Length(1, 512)])

    year = StringField('year achieved', 
            validators = [DataRequired(), Length(1, 16)])

    submit = SubmitField('submit')
