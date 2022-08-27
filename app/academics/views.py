import flask
from . import academics
from .. import db
from .forms import KCSEResultsForm, InitiateExamForm
from ..models import KCSE_Results, exam


@academics.route('/initiate_exam', methods = ['GET', 'POST'])
def initiate_exam():
    form = InitiateExamForm()

    if form.validate_on_submit():
        EXAM = exam(
                exam_title = form.title.data
                )
        db.session.add(EXAM)
        db.session.commit()

        flask.flash('%r initiated successfully.'%(form.title.data))
        return flask.redirect(flask.url_for('academics.initiate_exam'))

    return flask.render_template('academics/initiate_exam.html', form = form)


@academics.route('/update_KCSE_results')
def update_KCSE_Results():
    exams = KCSE_Results.query.order_by(KCSE_Results.KCSE_ID.desc()).all()
    return flask.render_template('academics/update_KCSE_Results.html', exams = exams)

@academics.route('add_KCSE_Results', methods = ['GET', 'POST'])
def add_KCSE_Results():
    form = KCSEResultsForm()

    if form.validate_on_submit():
        KCSE_RESULTS = KCSE_Results(
                A = form.A.data, 
                A_minus = form.A_minus.data,
                B_plus = form.B_plus.data,
                B = form.B.data,
                B_minus = form.B_minus.data,
                C_plus = form.C_plus.data,
                C = form.C.data,
                C_minus = form.C_plus.data,
                D_plus = form.D_plus.data,
                D = form.D.data,
                D_minus = form.D_minus.data,
                E = form.E.data,
                year = form.year.data
                )
        db.session.add(KCSE_RESULTS)
        db.session.commit()

        flask.flash('Data saved successfully.')
        return flask.redirect(flask.url_for('academics.homepage'))

    return flask.render_template('academics/add_KCSE_Results.html', form = form)


@academics.route('/homepage')
def homepage():
    entry = KCSE_Results.query.filter_by(KCSE_ID = 1).first()
    exams = exam.query.order_by(exam.exam_id.desc()).all()

    return flask.render_template('academics/homepage.html', entry = entry, exams = exams)
