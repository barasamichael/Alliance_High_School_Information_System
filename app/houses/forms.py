from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Length, Regexp, DataRequired
from ..models import house

class UpdateProfileImageForm(FlaskForm):
    file = FileField('select image file', validators = [FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Select image files only.')])
    submit = SubmitField('submit')


class HouseRegistrationForm(FlaskForm):
    house_name = StringField('house name', 
        validators = [DataRequired(), Length(1, 64), 
        Regexp('^[A-Za-z][A-Za-z]',0,'Non-alaphabetical characters not allowed.')])

    year_established = StringField('year established', validators = 
            [DataRequired(), Length(1, 32)])

    opened_by = StringField('opened by', validators = 
            [DataRequired(), Length(1, 64)])

    motto = StringField('house motto', validators = 
            [DataRequired(), Length(1, 128)])

    bed_cover = StringField('bed cover', validators = 
            [DataRequired(), Length(1, 64)])

    sister_house = StringField('sister house', validators = 
            [DataRequired(), Length(1, 64)])

    submit = SubmitField('submit')

    def validate_house_name(self, field):
        if house.query.filter_by(house_title = field.data).first():
            raise ValidationError('House already registered!!!')

    def validate_bed_cover(self, field):
        if house.query.filter_by(bed_cover = field.data).first():
            raise ValidationError('Bed cover already in use by another house.')

    def validate_sister_house(self, field):
        if house.query.filter_by(sister_house = field.data).first():
            raise ValidationError('Sister house already assigned to another')



