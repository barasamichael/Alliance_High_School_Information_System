import os
import flask, imghdr
from flask import current_app
from werkzeug.utils import secure_filename
from . import clubs
from .. import db

from .forms import (ClubRegistrationForm, AchievementRegistrationForm, 
        FounderRegistrationForm, EventRegistrationForm, ClubWallPaperForm, 
        RegisterSpeakerForm, RegisterClubScheduleForm, ClubEventWallPaperForm)

from ..models import (club, student, founder, achievement, event, speaker, 
        club_schedule)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    
    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@clubs.route('/club_profile/schedule/<int:club_id>', methods = ['GET', 'POST'])
def register_club_schedule(club_id):
    form = RegisterClubScheduleForm()

    if form.validate_on_submit():
        schedule = club_schedule(
                day = form.day.data,
                description = form.description.data,
                start_time = form.start_time.data,
                end_time = form.end_time.data,
                club_id = club_id
                )
        db.session.add(schedule)
        db.session.commit()

        flask.flash('Schedule updated successfully.')
        return flask.redirect(flask.url_for('clubs.register_club_schedule', 
            club_id = club_id))

    return flask.render_template('clubs/register_club_schedule.html', 
            club_id = club_id, form = form)



@clubs.route('/event_profile/register_speaker/<int:event_id>', 
        methods = ['GET', 'POST'])
def register_event_speaker(event_id):
    form = RegisterSpeakerForm()

    if form.validate_on_submit():
        speaker_1 = speaker(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                email_address = form.email_address.data,
                profession = form.profession.data,
                event_id = event_id
                )
        db.session.add(speaker_1)
        db.session.commit()

        flask.flash('Speaker %r registered successfully.'%form.last_name.data)
        return flask.redirect(flask.url_for('clubs.register_event_speaker', 
            event_id = event_id))

    return flask.render_template('clubs/register_event_speaker.html', 
            event_id = event_id, form = form)


@clubs.route('/event_profile/upload_event_images/<int:event_id>', 
        methods = ['GET', 'POST'])
def upload_event_images(event_id):
    event_1 = event.query.filter_by(event_id = event_id).first()
    folder = event_1.title
    folder = os.path.join(current_app.config['CLUB_EVENT_UPLOAD_PATH'],\
            folder.strip())

    files = os.listdir(os.path.join(
        current_app.config['CLUB_EVENT_UPLOAD_PATH'],folder))

    if flask.request.method == 'POST':
        uploaded_file = flask.request.files['file']
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] \
                or file_ext != validate_image(uploaded_file.stream):
                    return 'Invalid Image', 400
            uploaded_file.save(os.path.join(folder, filename))

    return flask.render_template('clubs/upload_event_images.html', 
            event_id = event_id, files = files)


@clubs.route('/event_profile/upload_event_wall_picture/<int:event_id>', 
        methods = ['GET', 'POST'])
def upload_event_wall_picture(event_id):
    event_1 = event.query.filter_by(event_id = event_id).first()
    folder = event_1.title
    folder = os.path.join(current_app.config['CLUB_EVENT_UPLOAD_PATH'], folder.strip())

    form = ClubEventWallPaperForm()
    if form.validate_on_submit():

        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] \
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

            uploaded_file.save(os.path.join(folder, filename))

        event_1.associated_image = filename
        db.session.add(event_1)
        db.session.commit()

        flask.flash('Image set successfully.')
        return flask.redirect(flask.url_for('clubs.event_profile',
            event_id=event_id))

    return flask.render_template('clubs/upload_event_image.html', form = form)


@clubs.route('/club_profile/upload_club_wall_picture/<int:club_id>', 
        methods = ['GET', 'POST'])
def upload_club_wall_picture(club_id):
    club_1 = club.query.filter_by(club_id = club_id).first()
    folder = club_1.club_name
    folder = os.path.join(current_app.config['UPLOAD_PATH'], folder.strip())

    form = ClubWallPaperForm()
    if form.validate_on_submit():

        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] \
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

            uploaded_file.save(os.path.join(folder, filename))

        club_1.associated_image = filename
        db.session.add(club_1)
        db.session.commit()

        flask.flash('Image set successfully.')
        return flask.redirect(flask.url_for('clubs.club_profile', club_id=club_id))

    return flask.render_template('clubs/upload_club_image.html', form = form)



@clubs.route('club_profile/event_profile/<int:event_id>', 
        methods = ['GET', 'POST'])
def event_profile(event_id):
    event_1 = event.query.filter_by(event_id = event_id)\
            .join(club, club.club_id == event.club_id)\
            .add_columns(
                    event.event_id,
                    event.title,
                    event.description,
                    event.associated_image,
                    club.associated_image.label('club_image'),
                    event.start_time,
                    event.end_time,
                    event.venue,
                    club.club_name,
                    event.club_id
                    ).first()

    folder = event_1.title.strip()
    club_folder = event_1.club_name.strip()

    speakers = speaker.query.filter_by(event_id = event_id)\
            .order_by(speaker.first_name.desc()).all()
    image_files = os.listdir(os.path.join(
        current_app.config['CLUB_EVENT_UPLOAD_PATH'],folder))
            
    return flask.render_template('clubs/event_profile.html', event = event_1, 
        speakers = speakers, folder = folder, images = image_files, club_folder = club_folder)


@clubs.route('/club_profile/event/<int:club_id>', methods = ['GET', 'POST'])
def club_event(club_id):

    form = EventRegistrationForm()
    if form.validate_on_submit():
        event_1 = event(
                title = form.title.data,
                description = form.description.data,
                date_scheduled = form.date_scheduled.data,
                venue = form.venue.data,
                start_time = form.start_time.data,
                end_time = form.end_time.data,
                club_id = club_id
                )

        db.session.add(event_1)
        db.session.commit()

        try:
            file_name = form.title.data
            os.mkdir(os.path.join(current_app.config['CLUB_EVENT_UPLOAD_PATH'],
                file_name.strip()))
        except:
            flask.flash('Folder already exists.')

        flask.flash('Event registered successfully.')
        return flask.redirect(flask.url_for('clubs.club_event', club_id = club_id))

    return flask.render_template('clubs/register_event.html', form = form, 
            club_id = club_id)


@clubs.route('/club_profile/founder/<int:club_id>', methods = ['GET', 'POST'])
def club_founder(club_id):

    form = FounderRegistrationForm()
    if form.validate_on_submit():
        founder_1 = founder(
                names = form.names.data,
                gender = form.gender.data,
                email_address = form.email_address.data,
                club_id = club_id

                )

        db.session.add(founder_1)
        db.session.commit()

        flask.flash('Founder %r saved successfully.'%(form.names.data))
        return flask.redirect(flask.url_for('clubs.club_founder', club_id=club_id))

    return flask.render_template('clubs/register_founder.html', form = form, 
            club_id = club_id)



@clubs.route('/club_profile/achievement/<int:club_id>', methods = ['GET', 'POST'])
def club_achievement(club_id):
    form = AchievementRegistrationForm()

    if form.validate_on_submit():

        achievement_1 = achievement(
                description = form.description.data,
                year_achieved = form.year_achieved.data,
                club_id = club_id
                )

        db.session.add(achievement_1)
        db.session.commit()

        flask.flash('Achievement recorded successfully.')
        return flask.redirect(flask.url_for('clubs.club_achievement', 
            club_id = club_id))

    return flask.render_template('clubs/register_achievement.html', form = form, 
            club_id = club_id)


@clubs.route('/club_profile/<int:club_id>', methods = ['GET', 'POST'])
def club_profile(club_id):
    club_1 = club.query.filter_by(club_id = club_id).first()

    folder = club_1.club_name.strip()

    founders = founder.query.filter_by(club_id = club_id).all()
    achievements = achievement.query.filter_by(club_id = club_id)\
            .order_by(achievement.year_achieved.desc()).all()

    events = event.query.filter_by(club_id = club_id)\
            .order_by(event.date_scheduled.desc()).all()
            
    schedules = club_schedule.query.filter_by(club_id = club_1.club_id)\
            .order_by(club_schedule.schedule_id.desc()).all()

    return flask.render_template('clubs/club_profile.html', club = club_1, 
            achievements = achievements, founders = founders, events = events, 
            schedules = schedules, folder = folder)


@clubs.route('/register_club', methods = ["GET", "POST"])
def register_club():

    form = ClubRegistrationForm()
    if form.validate_on_submit():
        club_1 = club(
                club_name = form.club_name.data,
                year_founded = form.year_founded.data,
                mission = form.mission.data,
                vision = form.vision.data,
                venue = form.venue.data, 
                email_address = form.email_address.data,
                about_us = form.about_us.data
                )
        db.session.add(club_1)
        db.session.commit()

        #create a club folder to hold club images
        try:
            file_name = form.club_name.data
            os.mkdir(os.path.join(current_app.config['OBC_UPLOAD_PATH'], 
                file_name.strip()))
        except:
            flask.flash('Folder already exists.')

        flask.flash('%r club registered successfully'%form.club_name.data)
        return flask.redirect(flask.url_for('clubs.clubs'))

    return flask.render_template('clubs/register_club.html', form = form)


@clubs.route('/clubs', methods = ['GET', 'POST'])
def clubs():
    clubs = club.query.order_by(club.club_name.desc()).all()

    return flask.render_template('clubs/clubs.html', clubs = clubs)

