import flask, os, imghdr
from . import sports
from .. import db

from werkzeug.utils import secure_filename

from .forms import (RegisterSportForm, RegisterPositionForm, RegisterTeamForm, 
        RegisterNotificationForm, RegisterEventForm , RegisterCoachForm, 
        SportAssignmentForm, UpdateSportProfileImageForm, RegisterSchoolForm)

from ..models import (sport, sport_notification, sport_team, sport_position, 
        sport_event, sport_coach, sport_assignment, teacher, school)

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@sports.route('/')
@sports.route('/homepage')
def homepage():
    sports = sport.query.order_by(sport.sport_name.asc()).all()
    return flask.render_template('sports/sports_homepage.html', sports = sports)


@sports.route('/register_school', methods = ['GET', 'POST'])
def register_school():
    form = RegisterSchoolForm()

    if form.validate_on_submit():
        School = school(
                title = form.title.data,
                nickname = form.nickname.data
                )
        db.session.add(School)
        db.session.commit()
        flask.flash(f'{form.nickname.data} added successfully.')
        return flask.redirect(flask.url_for('sports.register_school'))

    return flask.render_template('sports/register_school.html', form = form)


@sports.route('/school_nicknames')
def school_nicknames():
    schools = school.query.order_by(school.title.asc()).all()
    return flask.render_template('sports/school_nicknames.html', schools = schools)


@sports.route('/update_sport_profile_image/<int:sport_id>', 
        methods = ['GET', 'POST'])
def update_sport_profile_image(sport_id):
    Sport = sport.query.filter_by(sport_id = sport_id).first_or_404()

    form = UpdateSportProfileImageForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                        return flask.abort(400)

            uploaded_file.save(os.path.join(
                flask.current_app.config['SPORTS_UPLOAD_PATH'], filename))

        Sport.associated_image = filename
        db.session.add(Sport)
        db.session.commit()

        return flask.redirect(flask.url_for('sports.sport_profile', 
            sport_id = sport_id))

    return flask.render_template('sports/update_sport_profile_image.html', 
            form = form)


@sports.route('/view_sports')
def view_sports():
    sports = sport.query.order_by(sport.sport_name.asc()).all()
    return flask.render_template('sports/view_sports.html', sports = sports)

@sports.route('/sport_profile/<int:sport_id>')
def sport_profile(sport_id):
    Sport = sport.query.filter_by(sport_id = sport_id).first_or_404()
    return flask.render_template('sports/sport_profile.html', sport = Sport)


@sports.route('/register_sport', methods = ['GET', 'POST'])
def register_sport():
    form = RegisterSportForm()

    if form.validate_on_submit():
        Sport = sport(
                sport_name = form.sport_name.data,
                year_established = form.year_established.data
                )
        db.session.add(Sport)
        db.session.commit()
        flask.flash(f'{form.sport_name.data} registered successfully.')
        return flask.redirect(flask.url_for('sports.register_sport'))

    return flask.render_template('sports/register_sport.html', form = form)


@sports.route('/register_coach/<int:sport_id>', methods = ['GET', 'POST'])
def register_coach(sport_id):
    Sport = sport.query.filter_by(sport_id = sport_id).first_or_404()

    form = RegisterCoachForm()

    if form.validate_on_submit():
        Coach = sport_coach(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                email_address = form.email_address.data,
                phone_no = form.phone_no.data,
                residential_address = form.residential_address.data,
                year_appointed = form.year_appointed.data,
                sport_id = Sport.sport_id
                )
        return flask.redirect(flask.url_for('sports.sport_profile', 
            sport_id = sport_id))

    return flask.render_template('sports/register_coach.html', form = form)


@sports.route('/register_team/<int:sport_id>', methods = ['GET', 'POST'])
def register_team(sport_id):
    Sport = sport.query.filter_by(sport_id = sport_id).first_or_404()

    form = RegisterTeamForm()

    if form.validate_on_submit():
        Team = sport_team(
                team_name = form.team_name.data,
                sport_id = Sport.sport_id 
                )
        db.session.add(Team)
        db.session.commit()

        flask.flash(f'{form.team_name.data} registered sucessfully')
        return flask.render_template(
                flask.url_for('sports/sport_profile', sport_id = sport_id))

    return flask.render_template('sports/register_team.html', form = form)


@sports.route('/register_position', methods = ['GET', 'POST'])
def register_position():
    return flask.render_template('sports/register_position.html', form = form)

@sports.route('/register_event', methods = ['GET', 'POST'])
def register_event():
    return flask.render_template('sports/register_event.html', form = form)

@sports.route('/register_notification', methods = ['GET', 'POST'])
def register_notification():
    return flask.render_template('sports/register_notification.html', form = form)

