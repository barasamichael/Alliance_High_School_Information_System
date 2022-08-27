import flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, Email
from wtforms.fields.html5 import DateField, TimeField

from ..models import subject, teacher


class SubjectSelectionForm(FlaskForm):
    subject_id = SelectField('select subject', validators = [DataRequired()])
    submit = SubmitField('submit')


class ClassSelectionForm(FlaskForm):
    class_id = SelectField('select class', validators = [DataRequired()])
    submit = SubmitField('submit')


class AssignTeacherForm(FlaskForm):
    teacher_id = SelectField('select teacher', validators = [DataRequired()])
    class_id = SelectField('select class', validators = [DataRequired()])
    submit = SubmitField('submit')


class SubjectAssignmentForm(FlaskForm):
    teacher_id = SelectField('select teacher', validators = [DataRequired()])
    submit = SubmitField('submit')



class RegisterDepartmentForm(FlaskForm):
    subject_title = StringField('enter department name', validators = [DataRequired(), 
        Length(1, 128)])
    phone_no = StringField('enter phone number', validators = [DataRequired(), 
        Length(1, 32)])
    email_address = StringField('enter email address', validators = [DataRequired(), 
        Length(1, 128), Email()])
    submit = SubmitField('submit')

    def validate_subject_title(self, field):
        if subject.query.filter_by(subject_title = field.data).first():
            raise ValidationError('department already exists. Try another name.')

    def validate_email_address(self, field):
        if subject.query.filter_by(email_address = field.data).first():
            raise ValidationError('email address already exists.')

    def validate_phone_no(self, field):
        if subject.query.filter_by(phone_no = field.data).first():
            raise ValidationError('phone number already exists.')


class RegisterTeacherForm(FlaskForm):
    first_name = StringField('first name', validators = [DataRequired(), Length(1, 64)])
    middle_name = StringField('middle name', validators = [Length(1, 64)])
    last_name = StringField('last name', validators = [Length(1, 64)])
    gender = SelectField('gender', choices = [('Male', 'Male'), ('Female', 'Female')], 
            validators = [DataRequired()])

    TSC_no = StringField('TSC number', validators = [DataRequired(), Length(1, 64)])
    national_id_no = IntegerField('national ID number', validators = [DataRequired()])

    date_of_birth = DateField('date of birth', validators = [DataRequired()])
    email_address = StringField('email address', validators = [DataRequired(), 
        Length(1, 128), Email()])
    phone_no = StringField('phone number', validators = [DataRequired(), Length(1, 32)])
    residential_address = StringField('residential address', 
            validators = [DataRequired(), Length(1, 255)])

    submit = SubmitField('submit')

    def validate_email_address(self, field):
        if teacher.query.filter_by(email_address = field.data).first():
            raise ValidationError('email address already exists.')

    def validate_TSC_no(self, field):
        if teacher.query.filter_by(TSC_no = field.data).first():
            raise ValidationError('TSC number already exists.')

    def validate_phone_no(self, field):
        if teacher.query.filter_by(phone_no = field.data).first():
            raise ValidationError('phone number already exists.')

    def validate_national_id_no(self, field):
        if teacher.query.filter_by(national_id_no = field.data).first():
            raise ValidationError('national id number already exists.')
