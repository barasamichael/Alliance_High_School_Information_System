import flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields.html5 import DateField, TimeField

from ..models import student, classroom

class RegisterClassForm(FlaskForm):
    title = StringField('enter name of class', validators = [DataRequired(),Length(1,64)])
    submit = SubmitField('submit')

    def validate_title(self, field):
        if classroom.query.filter_by(title = field.data).first():
            raise ValidationError('class already exists.')


class DisciplineForm(FlaskForm):
    offence = StringField('offense', validators = [DataRequired(), 
        Length(1, 1024)])
    punishment = StringField('punishment', validators = [DataRequired(), 
        Length(1, 255)])
    overseer = StringField('overseer', validators = [DataRequired(), 
        Length(1, 255)])
    date = DateField('date of punishment', validators = [DataRequired()])
    start_time = TimeField('start time', validators = [DataRequired()])
    end_time = TimeField('end time', validators = [DataRequired()])

    submit = SubmitField('submit')



class StudentRegistrationForm(FlaskForm):
    first_name = StringField('first name', 
            validators = [DataRequired(), Length(1, 64)])
    middle_name = StringField('middle name', 
            validators = [DataRequired(), Length(1, 64)])
    last_name = StringField('last name', validators = [Length(0, 64)])

    gender = SelectField('gender', validators = [DataRequired()], 
            choices = [('male', 'male'),('female', 'female')])
    date_of_birth = DateField('date of birth', validators = [DataRequired()])
    nationality = SelectField('nationality', validators = [DataRequired()])
    nemis = StringField('nemis', validators = [Length(1, 255)])
    phone_no = StringField('phone number', 
            validators = [DataRequired(), Length(1, 32)])
    email_address = StringField('email address', validators = [DataRequired()])
    residence = StringField('residence', 
            validators = [DataRequired(), Length(1, 128)])
    house_id = SelectField('house', validators = [DataRequired()])

    submit = SubmitField('submit')

    def validate_email_address(self, field):
        if student.query.filter_by(email_address = field.data).first():
            raise ValidationError('email address already exists.')

    def validate_nemis(self, field):
        if student.query.filter_by(nemis = field.data).first():
            raise ValidationError('UPI number already exists.')

    def validate_phone_no(self, field):
        if student.query.filter_by(phone_no = field.data).first():
            raise ValidationError('phone number already exists.')

