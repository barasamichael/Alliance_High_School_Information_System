import flask
import iso3166
from flask import current_app
from . import students
from .. import db
from .forms import StudentRegistrationForm, DisciplineForm, RegisterClassForm
from ..models import student, house, punishment, classroom, nurse, medical_record


@students.route('/student_profile/add_punishment/<int:admission_no>', 
        methods = ['GET', 'POST'])
def add_punishment(admission_no):

    form = DisciplineForm()
    if form.validate_on_submit():
        punishment_1 = punishment(
                offence = form.offence.data,
                punishment = form.punishment.data,
                overseer = form.overseer.data,
                date = form.date.data,
                start_time = form.start_time.data,
                end_time = form.end_time.data,
                admission_no = admission_no
                )

        db.session.add(punishment_1)
        db.session.commit()

        flask.flash('Punishment added successfully.')
        return flask.redirect(flask.url_for('students.student_profile', 
            admission_no = admission_no))

    return flask.render_template('students/add_punishment.html', form = form)


@students.route('/student_profile/academics/<int:admission_no>', 
        methods = ['GET', 'POST'])
def academics(admission_no):
    response = flask.make_response(flask.redirect(
        flask.url_for('students.student_profile', admission_no = admission_no)
        )
    )
    response.set_cookie('tab_var', '1', max_age = 60*60)

    return response

@students.route('/student_profile/discipline/<int:admission_no>',
        methods = ['GET', 'POST'])
def discipline(admission_no):
    response = flask.make_response(flask.redirect(
        flask.url_for('students.student_profile', admission_no = admission_no)
        )
    )
    response.set_cookie('tab_var', '2', max_age = 60*60)

    return response

@students.route('/student_profile/sports/<int:admission_no>',
        methods = ['GET', 'POST'])
def sports(admission_no):
    response = flask.make_response(flask.redirect(
        flask.url_for('students.student_profile', admission_no = admission_no)
        )
    )
    response.set_cookie('tab_var', '3', max_age = 60*60)

    return response

@students.route('/student_profile/co_curricular/<int:admission_no>',
        methods = ['GET', 'POST'])
def co_curricular(admission_no):
    response = flask.make_response(flask.redirect(
        flask.url_for('students.student_profile', admission_no = admission_no)
        )
    )
    response.set_cookie('tab_var', '4', max_age = 60*60)

    return response

@students.route('/student_profile/accounts/<int:admission_no>',
        methods = ['GET', 'POST'])
def accounts(admission_no):
    response = flask.make_response(flask.redirect(
        flask.url_for('students.student_profile', admission_no = admission_no)
        )
    )
    response.set_cookie('tab_var', '5', max_age = 60*60)

    return response


@students.route('/student_profile/health/<int:admission_no>',
        methods = ['GET', 'POST'])
def health(admission_no):
    response = flask.make_response(flask.redirect(
        flask.url_for('students.student_profile', admission_no = admission_no)
        )
    )
    response.set_cookie('tab_var', '6', max_age = 60*60)

    return response


@students.route('/student_profile/<int:admission_no>', methods = ['GET', 'POST'])
def student_profile(admission_no):
    student_1 = student.query.filter_by(admission_no = admission_no)\
        .join(house, house.house_id == student.house_id)\
            .add_columns(student.admission_no,
                    student.first_name,
                    student.last_name,
                    student.middle_name,
                    student.gender,
                    student.residence,
                    student.phone_no,
                    student.date_of_birth,
                    student.email_address,
                    student.nationality,
                    student.nemis,
                    house.house_title).first()

    tab_variable = 1
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    if tab_variable == 1:
        return flask.render_template('students/student_profile.html',
                student=student_1,tab_variable = tab_variable)

    elif tab_variable == 2:

        punishments = punishment.query.filter_by(admission_no = admission_no).all()

        return flask.render_template('students/student_profile.html',\
                student=student_1,tab_variable = tab_variable, 
                punishments = punishments)

    elif tab_variable == 3:
        return flask.render_template('students/student_profile.html',\
                student=student_1, tab_variable = tab_variable)

    elif tab_variable == 4:
        return flask.render_template('students/student_profile.html',\
                student=student_1,tab_variable = tab_variable)

    elif tab_variable == 5:
        return flask.render_template('students/student_profile.html',\
                student=student_1,tab_variable = tab_variable)

    elif tab_variable == 6:
        records = medical_record.query.filter_by(student_id = student.admission_no)\
                .join(nurse, nurse.nurse_id == medical_record.nurse_id)\
                .add_columns(
                        medical_record.record_id,
                        medical_record.date_created,
                        nurse.first_name,
                        nurse.middle_name,
                        nurse.last_name,
                        nurse.nurse_id
                        ).order_by(medical_record.date_created.desc()).all()
        return flask.render_template('students/student_profile.html',
                student=student_1,tab_variable = tab_variable, records = records)
    return flask.render_template('students/student_profile.html',
                student=student_1,tab_variable = tab_variable)


@students.route('/view_students', methods = ['GET', 'POST'])
def view_students():
    page = flask.request.args.get('page', 1, type = int)
    pagination = student.query.order_by(student.admission_no.desc())\
            .join(house, house.house_id == student.house_id)\
            .add_columns(
                    student.admission_no,
                    student.first_name,
                    student.last_name,
                    student.middle_name,
                    student.gender,
                    student.date_of_birth,
                    student.email_address,
                    house.house_title
                    )\
            .paginate(page, per_page = current_app.config['FLASKY_POSTS_PER_PAGE'], 
                    error_out = False)
    
    students = pagination.items

    return flask.render_template('students/view_students.html', 
            students = students, pagination = pagination)


@students.route('/register_student', methods = ['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()

    country_list = [(country.name, country.name) for country in iso3166.countries]
    house_list = [(item.house_id, item.house_title) for item in house.query.all()]
    
    form.nationality.choices = country_list
    form.house_id.choices = house_list

    if form.validate_on_submit():
        student_1 = student(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                middle_name = form.middle_name.data, 
                gender = form.gender.data,
                date_of_birth = form.date_of_birth.data,
                nationality = form.nationality.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residence = form.residence.data,
                nemis = form.nemis.data,
                house_id = form.house_id.data,
                )

        db.session.add(student_1)
        db.session.commit()

        flask.flash(f'{form.first_name.data} {form.last_name.data} {form.middle_name.data} saved succesfully.')
        return flask.redirect(flask.url_for('students.view_students'))

    return flask.render_template('students/register_student.html', form = form)


@students.route('/view_classrooms')
def view_classrooms():
    classes = classroom.query.order_by(classroom.class_id.desc()).all()
    return flask.render_template('students/view_classrooms.html', classes = classes)


@students.route('/register_class', methods = ['GET', 'POST'])
def register_class():
    form = RegisterClassForm()

    if form.validate_on_submit():
        CLASS = classroom(
                title = form.title.data
                )

        db.session.add(CLASS)
        db.session.commit()

        flask.flash('Class {form.title.data}  registered successfully.')
        return flask.redirect(flask.url_for('students.view_classrooms'))

    return flask.render_template('students/register_class.html', form = form)
