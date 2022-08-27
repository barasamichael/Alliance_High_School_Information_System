import flask
from . import sanatorium
from .. import db
from .forms import (RegisterNurseForm, StudentHealthLoginForm, DiagnosisForm, 
        AddMedicalStockForm)
from ..models import (nurse, student,medical_record, diagnosis, medication_stock, 
        current_stock)


@sanatorium.route('/view_medicine_stock', methods = ['GET', 'POST'])
def view_medicine_stock():
    page = flask.request.args.get('page', 1, type = int)
    pagination = medication_stock.query.order_by(medication_stock.description.asc())\
            .paginate(page, per_page = flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
                    error_out = False)

    medicine = pagination.items

    return flask.render_template('sanatorium/view_medicine_stock.html', 
            medicine = medicine, pagination = pagination)


@sanatorium.route('/add_medical_stock', methods = ['GET', 'POST'])
def add_medical_stock():
    form = AddMedicalStockForm()

    if form.validate_on_submit():
        stock = medication_stock(
                description = form.description.data,
                units = form.units.data
                )
        db.session.add(stock)
        db.session.commit()

        flask.flash('Stock added successfully.')
        return flask.redirect(flask.url_for('sanatorium.add_medical_stock'))

    return flask.render_template('sanatorium/add_medical_stock.html', form = form)


@sanatorium.route('/update_medical_stock', methods = ['GET', 'POST'])
def update_medical_stock():
    form = UpdateMedicineStockForm(FlaskForm)

    if form.validate_on_submit():
        update = current_stock(
                stock_id = form.stock_id.data,
                quantity = form.quantity.data
                )

        db.session.add(update)
        db.session.commit()

        flask.flash('stock update successful.')
        return flask.redirect(flask.url_for('sanatorium.update_medical_stock'))

    return flask.render_template('sanatorium/update_medical_stock.html', form = form) 


@sanatorium.route('/record_diagnosis/<int:record_id>', methods = ['GET', 'POST'])
def record_diagnosis(record_id):
    form = DiagnosisForm()

    if form.validate_on_submit():
        DIAGNOSIS = diagnosis(
                description = form.description.data,
                record_id = record_id
                )

        db.session.add(DIAGNOSIS)
        db.session.commit()

        return flask.redirect(flask.url_for('sanatorium.record_diagnosis', 
            record_id = record_id))

    return flask.render_template('sanatorium/diagnosis.html', form = form)


@sanatorium.route('/new_medical_record/<int:adm_no>')
def new_medical_record(adm_no):
    record = medical_record(student_id = adm_no, nurse_id = 1)
    db.session.add(record)
    db.session.commit()

    record_1 = medical_record.query.filter(medical_record.student_id == adm_no, 
        medical_record.nurse_id == 1).order_by(medical_record.record_id.desc()).first()

    return flask.redirect(flask.url_for('sanatorium.record_diagnosis', 
        record_id = record_1.record_id))


@sanatorium.route('/health_login', methods = ['GET', 'POST'])
def health_login():
    form = StudentHealthLoginForm()

    if form.validate_on_submit():
        if student.query.filter_by(admission_no = form.adm_no.data).first():
            return flask.redirect(flask.url_for('students.health', 
                admission_no = form.adm_no.data))

        flask.flash('student admission number %r does not exist.'%(form.adm_no.data))
        return flask.redirect(flask.url_for('sanatorium.health_login'))

    return flask.render_template('sanatorium/health_login.html', form = form)


@sanatorium.route('/nurse_profile/<int:nurse_id>', methods = ['GET', 'POST'])
def nurse_profile(nurse_id):
    nurse_1 = nurse.query.filter_by(nurse_id = nurse_id).first()
    return flask.render_template('sanatorium/nurse_profile.html', nurse = nurse_1)


@sanatorium.route('/view_nurses', methods = ['GET', 'POST'])
def view_nurses():
    nurses = nurse.query.all()
    return flask.render_template('sanatorium/view_nurses.html', nurses = nurses)


@sanatorium.route('/register_nurse', methods = ['GET', 'POST'])
def register_nurse():
    form = RegisterNurseForm()

    if form.validate_on_submit():
        NURSE = nurse(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residential_address = form.residential_address.data,
                national_id_no = form.national_id_no.data,
                status = form.status.data,
                date_of_birth = form.date_of_birth.data
                )

        db.session.add(NURSE)
        db.session.commit()

        flask.flash('%r %r %r registered successfully as an Alliance High School Nurse'%(
            form.first_name.data, form.middle_name.data, form.last_name.data))
        return flask.redirect(flask.url_for('sanatorium.view_nurses'))

    return flask.render_template('sanatorium/register_nurse.html', form = form)

@sanatorium.route('/homepage')
def homepage():
    return flask.render_template('sanatorium/homepage.html')
