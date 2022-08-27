import flask, imghdr, os
from flask import current_app
from werkzeug.utils import secure_filename

from . import obc
from .. import db

from .forms import (RegisterOBCForm, RegisterObcEventForm, ObcAchievementForm, 
        ObcProfileImageForm, UpdateOBCForm)
from ..models import obc as obc_db, house, obc_event, obc_achievement

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@obc.route('/homepage')
def obc_homepage():
    members = obc_db.query.filter_by(status = 'member')\
            .join(house, house.house_id == obc_db.house_id)\
            .add_columns(
                    obc_db.adm_no,
                    obc_db.first_name,
                    obc_db.last_name,
                    obc_db.middle_name,
                    obc_db.email_address,
                    obc_db.year,
                    obc_db.profession,
                    house.house_title,
                    obc_db.obc_id
                    ).order_by(obc_db.adm_no.desc()).all()

    obcs = obc_db.query.filter(obc_db.status != 'member')\
            .order_by(obc_db.adm_no.desc())\
            .all()

    events = obc_event.query.order_by(obc_event.date_scheduled.desc()).all()

    return flask.render_template('obc/obc_homepage.html', members = members, 
            obcs = obcs, events = events)


@obc.route('/register_member', methods = ['GET', 'POST'])
def register_member():
    houses = [(item.house_id, item.house_title) for item in house.query.all()]

    form = RegisterOBCForm()
    
    form.house_id.choices = houses
    
    if form.validate_on_submit():
        member = obc_db(
                adm_no = form.admission_no.data,
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                email_address = form.email_address.data,
                residential_address = form.residential_address.data,
                phone_no = form.phone_no.data,
                year = form.year.data,
                date_of_birth = form.date_of_birth.data,
                profession = form.profession.data,
                house_id = form.house_id.data,
                status = 'member'
                )

        db.session.add(member)
        db.session.commit()

        flask.flash('Mr. %r is now a member of the AHS OBC'%form.last_name.data)
        return flask.redirect(flask.url_for('obc.register_member'))

    return flask.render_template('obc/register_member.html', form = form)


@obc.route('/register_event', methods = ['GET', 'POST'])
def register_event():

    form = RegisterObcEventForm()
    if form.validate_on_submit():
        event = obc_event(
                title = form.title.data,
                description = form.description.data,
                date_scheduled = form.date_scheduled.data,
                start_time = form.start_time.data,
                end_time = form.end_time.data,
                venue = form.venue.data
                )

        db.session.add(event)
        db.session.commit()

        #create an event folder to hold club images
        try:
            file_name = form.title.data
            os.mkdir(os.path.join(current_app.config['EVENTS_UPLOAD_PATH'],
                file_name.strip()))
        except:
            flask.flash('Folder already exists.')

        flask.flash('Event registered successfully.')
        return flask.redirect(flask.url_for('obc.register_event'))

    return flask.render_template('obc/register_event.html', form = form)


@obc.route('/event_profile/<int:event_id>', methods = ['GET', 'POST'])
def event_profile(event_id):
    event = obc_event.query.filter_by(event_id = event_id).first()
    others = obc_event.query.filter(obc_event.event_id != event.event_id)\
            .order_by(obc_event.date_scheduled.desc()).all()

    folder = event.title.strip()

    return flask.render_template('obc/event_profile.html', event = event, 
            others = others, folder = folder)


@obc.route('/register_obc_achievement/<int:obc_id>', methods = ['GET', 'POST'])
def register_obc_achievement(obc_id):
    form = ObcAchievementForm()

    if form.validate_on_submit():
        achievement = obc_achievement(
                description = form.description.data,
                year = form.year.data,
                obc_id = obc_id
                )

        db.session.add(achievement)
        db.session.commit()

        flask.flash('Achievement recorded successfully.')
        return flask.redirect(flask.url_for('obc.register_obc_achievement', obc_id = obc_id))

    return flask.render_template('obc/register_obc_achievement.html', form = form, 
            obc_id = obc_id)


@obc.route('/obc_profile/<int:obc_id>', methods = ['GET', 'POST'])
def obc_profile(obc_id):
    user = obc_db.query.filter_by(obc_id = obc_id)\
            .join(house, house.house_id == obc_db.house_id)\
            .add_columns(
                    obc_db.obc_id,
                    obc_db.adm_no,
                    obc_db.first_name,
                    obc_db.last_name,
                    obc_db.middle_name,
                    obc_db.gender,
                    obc_db.email_address,
                    obc_db.residential_address,
                    obc_db.phone_no,
                    obc_db.profession,
                    obc_db.associated_image,
                    obc_db.year,
                    obc_db.date_of_birth,
                    obc_db.status,
                    house.house_title
                    ).first()

    achievements = obc_achievement.query.filter_by(obc_id = obc_id).all()

    return flask.render_template('obc/obc_profile.html', user = user, 
            achievements = achievements)


@obc.route('/update_obc_profile_photo<int:obc_id>', methods = ['GET', 'POST'])
def update_obc_profile_photo(obc_id):
    user = obc_db.query.filter_by(obc_id = obc_id).first()
    folder = os.path.join(current_app.config['EVENTS_UPLOAD_PATH'], 'profiles')

    form = ObcProfileImageForm()
    if form.validate_on_submit():

        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] \
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

            uploaded_file.save(os.path.join(folder, filename))

        user.associated_image = filename
        db.session.add(user)
        db.session.commit()

        flask.flash('Profile image successfully updated.')
        return flask.redirect(flask.url_for('obc.obc_profile', obc_id = obc_id))

    return flask.render_template('obc/update_obc_profile_photo.html', form = form)


@obc.route('/update_obc_profile/<int:obc_id>', methods = ['GET', 'POST'])
def update_obc_profile(obc_id):
    user = obc_db.query.filter_by(obc_id = obc_id).first()
    houses = [(item.house_id, item.house_title) for item in house.query.all()]

    form = UpdateOBCForm()
    form.house_id.choices = houses

    if form.validate_on_submit():

        user.adm_no = form.admission_no.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.middle_name = form.middle_name.data
        user.gender = form.gender.data
        user.email_address = form.email_address.data
        user.residential_address = form.residential_address.data
        user.phone_no = form.phone_no.data
        user.house_id = form.house_id.data
        user.profession = form.profession.data
        user.status = form.status.data
        user.year = form.year.data

        db.session.add(user)
        db.session.commit()

        flask.flash('Profile updated successfully.')
        return flask.redirect(flask.url_for('obc.obc_profile', obc_id = obc_id))

    form.admission_no.data = user.adm_no
    form.email_address.data = user.email_address
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.middle_name.data = user.middle_name
    form.gender.data = user.gender
    form.date_of_birth.data = user.date_of_birth
    form.phone_no.data = user.phone_no
    form.residential_address.data = user.residential_address
    form.profession.data = user.profession
    form.house_id.data = user.house_id
    form.year.data = user.year
    form.status.data = user.status

    return flask.render_template('obc/update_obc_profile.html', form = form)



@obc.route('/update_event_image/<int:event_id>', methods = ['GET', 'POST'])
def update_event_image(event_id):

    event = obc_event.query.filter_by(event_id = event_id).first()
    folder = os.path.join(current_app.config['EVENTS_UPLOAD_PATH'], 
            event.title.strip())

    form = ObcProfileImageForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] \
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

            uploaded_file.save(os.path.join(folder, filename))

        event.associated_image = filename
        db.session.add(event)
        db.session.commit()

        flask.flash('Image updated successfully.')
        return flask.redirect(flask.url_for('obc.event_profile', 
            event_id = event_id))

    return flask.render_template('obc/update_event_image_profile.html', form = form)

