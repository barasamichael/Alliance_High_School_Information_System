import flask
from flask import current_app
from . import departments
from .. import db
from .forms import (RegisterDepartmentForm, RegisterTeacherForm, SubjectAssignmentForm, 
        AssignTeacherForm, SubjectSelectionForm, ClassSelectionForm)
from ..models import subject, teacher,subject_assignment, class_assignment, classroom

@departments.route('/select_class/<int:teacher_id>/<int:subject_id>', 
        methods = ['GET', 'POST'])
def select_class(teacher_id, subject_id):
    form = ClassSelectionForm()

    classes = subject_assignment.query.filter_by(teacher_id = teacher_id)\
            .join(subject, subject.subject_id == subject_assignment.subject_id)\
            .join(class_assignment, class_assignment.subject_assignment_id == subject_id)\
            .join(classroom, classroom.class_id == class_assignment.class_id)\
            .add_columns(
                    classroom.title, classroom.class_id
            ).order_by(classroom.title.asc()).all()

    form.class_id.choices = [((item.class_id), (item.title)) for item in classes]
    
    if form.validate_on_submit():
        return '<h3>Done</h3>'

    return flask.render_template('departments/select_class.html', form = form)


@departments.route('/select_subject/<int:teacher_id>', methods = ['GET', 'POST'])
def select_subject(teacher_id):
    form = SubjectSelectionForm()

    subjects = subject_assignment.query.filter_by(teacher_id = teacher_id)\
            .join(subject, subject.subject_id == subject_assignment.subject_id)\
            .add_columns(
                    subject.subject_title, subject_assignment.subject_assignment_id
            ).order_by(subject.subject_title.asc()).all()

    form.subject_id.choices = [((item.subject_assignment_id), (item.subject_title)) 
            for item in subjects]

    if form.validate_on_submit():
        return flask.redirect(flask.url_for('departments.select_class', 
            subject_id = form.subject_id.data, teacher_id = teacher_id))

    return flask.render_template('departments/select_subject.html', form = form)


@departments.route('/assign_teacher/<int:department_id>', methods = ['GET', 'POST'])
def assign_teacher(department_id):
    form = AssignTeacherForm()

    classes = classroom.query.order_by(classroom.title.asc()).all()
    form.class_id.choices = [((item.class_id), (item.title)) for item in classes]

    teachers = subject_assignment.query.filter_by(subject_id = department_id)\
            .join(teacher, teacher.teacher_id == subject_assignment.teacher_id)\
            .add_columns(
                    teacher.first_name, 
                    teacher.middle_name,
                    teacher.last_name,
                    subject_assignment.subject_assignment_id
                    ).order_by(teacher.first_name.asc()).all()

    form.teacher_id.choices = [((item.subject_assignment_id), (item.first_name + ' ' + 
        item.middle_name + ' ' + item.last_name)) for item in teachers]

    if form.validate_on_submit():
        assign_teacher = class_assignment(
                subject_assignment_id = form.teacher_id.data,
                class_id = form.class_id.data
                )

        db.session.add(assign_teacher)
        db.session.commit()

        flask.flash('Assignment successful.')
        return flask.redirect(flask.url_for('departments.department_profile', 
            department_id = department_id))

    return flask.render_template('departments/assign_teacher.html', form = form)


@departments.route('/add_teacher/<int:department_id>', methods = ['GET', 'POST'])
def add_teacher(department_id):
    form = SubjectAssignmentForm()

    teachers = [((item.teacher_id),(item.first_name+' '+item.middle_name+' '+
        item.last_name)) for item in teacher.query.all()]
    form.teacher_id.choices = teachers

    if form.validate_on_submit():

        if subject_assignment.query.filter(
                subject_assignment.subject_id == department_id,
                subject_assignment.teacher_id == form.teacher_id.data
                ).first():
            flask.flash('Teacher is already registered in the department.')
            return flask.redirect(flask.url_for('departments.department_profile', 
                department_id = department_id))

        teacher_assignment = subject_assignment(
                teacher_id = form.teacher_id.data,
                subject_id = department_id
                )
        db.session.add(teacher_assignment)
        db.session.commit()

        flask.flash('Assignment successful.')
        return flask.redirect(flask.url_for('departments.department_profile', 
            department_id = department_id))

    return flask.render_template('departments/add_teacher.html', form = form)


@departments.route('department_profile/<int:department_id>')
def department_profile(department_id):
    department = subject.query.filter_by(subject_id = department_id).first()

    teachers = subject_assignment.query.filter_by(subject_id = department_id)\
            .join(teacher, teacher.teacher_id == subject_assignment.teacher_id)\
            .add_columns(
                    teacher.first_name, teacher.middle_name,
                    teacher.last_name, teacher.gender, teacher.teacher_id,
                    teacher.TSC_no, teacher.national_id_no,
                    teacher.email_address, teacher.phone_no
                    ).order_by(teacher.first_name.asc()).all()

    assignments = subject_assignment.query.filter_by(subject_id = department_id)\
            .join(teacher, teacher.teacher_id == subject_assignment.teacher_id)\
            .join(class_assignment, class_assignment.subject_assignment_id 
                    == subject_assignment.subject_assignment_id)\
            .join(classroom, classroom.class_id == class_assignment.class_id)\
            .add_columns(
                    teacher.first_name, teacher.middle_name,
                    teacher.last_name, teacher.teacher_id,
                    classroom.title, class_assignment.date_created
                    ).order_by(teacher.first_name.asc()).all()

    return flask.render_template('departments/department_profile.html', 
            department = department, teachers = teachers, assignments = assignments)


@departments.route('/teacher_profile/<int:teacher_id>')
def teacher_profile(teacher_id):
    teacher_1 = teacher.query.filter_by(teacher_id = teacher_id).first()
    return flask.render_template('departments/teacher_profile.html', teacher = teacher_1)


@departments.route('/view_teachers')
def view_teachers():
    page = flask.request.args.get('page', 1, type = int)

    pagination = teacher.query.paginate(page, 
            per_page = current_app.config['FLASKY_POSTS_PER_PAGE'],error_out = False)
    teachers = pagination.items

    return flask.render_template('departments/view_teachers.html', teachers = teachers, 
            pagination = pagination)


@departments.route('/view_departments')
def view_departments():
    departments = subject.query.order_by(subject.subject_title.asc()).all()
    return flask.render_template('departments/view_departments.html', 
            departments = departments)


@departments.route('/register_teacher', methods = ['GET', 'POST'])
def register_teacher():
    form = RegisterTeacherForm()

    if form.validate_on_submit():
        TEACHER = teacher(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                date_of_birth = form.date_of_birth.data,
                email_address = form.email_address.data,
                residential_address = form.residential_address.data,
                TSC_no = form.TSC_no.data,
                national_id_no = form.national_id_no.data,
                phone_no = form.phone_no.data
                )

        db.session.add(TEACHER)
        db.session.commit()

        flask.flash('Teacher %r %r registered successfully.'%(form.first_name.data, 
            form.last_name.data))
        return flask.redirect(flask.url_for('departments.view_teachers'))

    return flask.render_template('departments/register_teacher.html', form = form)


@departments.route('/register_department', methods = ['GET', 'POST'])
def register_department():
    form = RegisterDepartmentForm()

    if form.validate_on_submit():
        department = subject(
                subject_title = form.subject_title.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data
                )

        db.session.add(department)
        db.session.commit()

        flask.flash('%r department registered successfully.'%(form.subject_title.data))
        return flask.redirect(flask.url_for('departments.view_departments'))

    return flask.render_template('departments/register_department.html', form = form)
