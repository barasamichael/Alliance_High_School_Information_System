import flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, Email
from wtforms.fields.html5 import DateField

from ..models import nurse, hospital


class UpdateMedicineStockForm(FlaskForm):
    stock_id = SelectField('medicine description', validators = [DataRequired()])
    quantity = IntegerField('quantity', validators = [DataRequired()])
    submit = SubmitField('submit')


class AddMedicalStockForm(FlaskForm):
    description = StringField('description', validators = [DataRequired(),Length(1, 64)])
    units = StringField('units', validators = [DataRequired(), Length(1, 32)])
    submit = SubmitField('submit')


class DiagnosisForm(FlaskForm):
    description = StringField('enter description', validators = [DataRequired(), 
        Length(1, 255)]) 
    submit = SubmitField('submit')

class StudentHealthLoginForm(FlaskForm):
    adm_no = IntegerField('enter student admission number', validators = [DataRequired()])
    submit = SubmitField('submit')


class RegisterNurseForm(FlaskForm):
    first_name = StringField('first name', validators = [DataRequired(), Length(1, 64)])
    middle_name = StringField('middle name', validators = [Length(1, 64)])
    last_name = StringField('last name', validators = [Length(1, 64)])
    gender = SelectField('gender', choices = [('Male', 'Male'), ('Female', 'Female')], 
            validators = [DataRequired()])

    national_id_no = IntegerField('national ID number', validators = [DataRequired()])

    date_of_birth = DateField('date of birth', validators = [DataRequired()])
    email_address = StringField('email address', validators = [DataRequired(), 
        Length(1, 128), Email()])
    phone_no = StringField('phone number', validators = [DataRequired(), Length(1, 32)])
    residential_address = StringField('residential address', 
            validators = [DataRequired(), Length(1, 255)])
    status = SelectField('current status (whether in active duty or not)', 
            choices = [(('active'), ('active')), (('inactive'), ('inactive'))], 
            validators = [DataRequired()])

    submit = SubmitField('submit')

    def validate_email_address(self, field):
        if nurse.query.filter_by(email_address = field.data).first():
            raise ValidationError('email address already exists.')

    def validate_phone_no(self, field):
        if nurse.query.filter_by(phone_no = field.data).first():
            raise ValidationError('phone number already exists.')

    def validate_national_id_no(self, field):
        if nurse.query.filter_by(national_id_no = field.data).first():
            raise ValidationError('national id number already exists.')
