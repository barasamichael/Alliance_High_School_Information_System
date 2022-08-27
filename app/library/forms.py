import flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, Email
from wtforms.fields.html5 import DateField

from ..models import (book, book_category, related_book, author_assignment, 
        publisher_contact, publisher, book_assignment, book_author)

class UpdateProfileImageForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Select image files only.')])

    submit = SubmitField('submit')


class UpdateBookCoverForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Select Image Files Only.')])

    submit = SubmitField('submit')


class AssignBookAuthorForm(FlaskForm):
    author_id = SelectField('select author', validators = [DataRequired()])
    submit = SubmitField('submit')


class RegisterRelatedBookForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 255)])
    book_category = SelectField('select category', validators = [DataRequired()])
    year_of_production = StringField('year of production', validators = [DataRequired()])
    publisher_id = SelectField('select publisher', validators = [DataRequired()])
    author_id = SelectField('select author', validators = [DataRequired()])

    submit = SubmitField('submit')


class AuthorAssignmentForm(FlaskForm):
    author_id = SelectField('select author', validators = [DataRequired()])
    submit = SubmitField('submit')


class PublisherContactForm(FlaskForm):
    contact_detail = StringField('enter contact', validators = [DataRequired(), Length(1, 128)])
    submit = SubmitField('submit')


class RegisterPublisherForm(FlaskForm):
    publisher_name = StringField('name', validators = [DataRequired(), Length(1, 255)])
    location = StringField('location', validators = [DataRequired(), Length(1, 255)])
    submit = SubmitField('submit')


class RegisterBookForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 255)])
    book_category = SelectField('category', validators = [DataRequired(), Length(1, 255)])
    year_of_production = StringField('year of production', validators = [DataRequired()])
    publisher_id = SelectField('publisher', validators = [DataRequired()])

    submit = SubmitField('submit')


class RegisterBookCategoryForm(FlaskForm):
    category_name = StringField('category name', validators = [DataRequired()])

    submit = SubmitField('submit')


class RegisterAuthorForm(FlaskForm):
    first_name = StringField('first name', validators = [DataRequired(), Length(1, 64)])
    middle_name = StringField('middle name', validators = [Length(1, 64)])
    last_name = StringField('last name', validators = [Length(1, 64)])
    gender = SelectField('gender', choices = [('Male', 'Male'), ('Female', 'Female')],
            validators = [DataRequired()])

    email_address = StringField('email address', validators = [DataRequired(),
        Length(1, 128), Email()])
    phone_no = StringField('phone number', validators = [DataRequired(), Length(1, 32)])
    residential_address = StringField('residential address',
            validators = [DataRequired(), Length(1, 255)])

    submit = SubmitField('submit')

