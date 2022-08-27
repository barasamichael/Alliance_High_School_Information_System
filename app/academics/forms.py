from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Length, Regexp, DataRequired

from ..models import KCSE_Results, exam

class KCSEResultsForm(FlaskForm):
    year = StringField('year KCSE done', validators = [DataRequired(), Length(1, 128)])

    A = IntegerField("number of A's")
    A_minus = IntegerField("number of A-'s")
    B_plus = IntegerField("number of B+'s")
    B = IntegerField("number of B's")
    B_minus = IntegerField("number of B-'s")
    C_plus = IntegerField("number of C+'s")
    C = IntegerField("number of C's")
    C_minus = IntegerField("number of C-'s")
    D_plus = IntegerField("number of D+'s")
    D = IntegerField("number of D's")
    D_minus = IntegerField("number of D-'s")
    E = IntegerField("number of E's")

    submit = SubmitField('submit')

    def validate_year(self, field):
        if KCSE_Results.query.filter_by(year= field.data).first():
            raise ValidationError('Results posted for this year already exist.')


class InitiateExamForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1,255)])
    submit = SubmitField('submit')

    def validate_title(self, field):
        if exam.query.filter_by(exam_title = field.data).first():
            raise ValidationError('Exam title cannot be the same as a past one.')
