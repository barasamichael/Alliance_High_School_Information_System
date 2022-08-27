import flask, os, imghdr
from werkzeug.utils import secure_filename
from . import houses
from .. import db
from .forms import HouseRegistrationForm, UpdateProfileImageForm
from ..models import house, student

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@houses.route('/update_house_profile_image/<int:house_id>', 
        methods = ['GET', 'POST'])
def update_house_profile_image(house_id):
    House = house.query.filter_by(house_id = house_id).first_or_404()

    form = UpdateProfileImageForm()

    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                        return flask.abort(400)

            uploaded_file.save(os.path.join(
                flask.current_app.config['HOUSES_UPLOAD_PATH'], filename))

        House.associated_image = filename
        db.session.add(House)
        db.session.commit()

        return flask.redirect(flask.url_for('houses.house_profile', 
            house_id = House.house_id))

    return flask.render_template('houses/update_house_profile_image.html', 
            form = form)


@houses.route('/house_profile/membership/<int:house_id>')
def membership(house_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('houses.house_profile', house_id = house_id)
        )
    )
    response.set_cookie('tab_var', '1', max_age = 60*60)

    return response


@houses.route('/house_profile/administration/<int:house_id>')
def administration(house_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('houses.house_profile', house_id = house_id)
        )
    )
    response.set_cookie('tab_var', '2', max_age = 60*60)

    return response


@houses.route('/house_profile/events/<int:house_id>')
def events(house_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('houses.house_profile', house_id = house_id)
        )
    )
    response.set_cookie('tab_var', '3', max_age = 60*60)

    return response


@houses.route('/house_profile/notifications/<int:house_id>')
def notifications(house_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('houses.house_profile', house_id = house_id)
        )
    )
    response.set_cookie('tab_var', '4', max_age = 60*60)

    return response


@houses.route('/house_profile/gallery/<int:house_id>')
def gallery(house_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('houses.house_profile', house_id = house_id)
        )
    )
    response.set_cookie('tab_var', '5', max_age = 60*60)

    return response


@houses.route('/house_profile/history/<int:house_id>')
def history(house_id):
    response = flask.make_response(flask.redirect(
        flask.url_for('houses.house_profile', house_id = house_id)
        )
    )
    response.set_cookie('tab_var', '6', max_age = 60*60)

    return response


@houses.route('/house_profile/<int:house_id>')
def house_profile(house_id):
    House = house.query.filter_by(house_id = house_id).first_or_404()

    tab_variable = 1
    
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    if tab_variable == 1:
        page = flask.request.args.get('page', 1, type = int)
        pagination = student.query.filter_by(house_id = House.house_id)\
            .order_by(student.admission_no.desc())\
            .paginate(page, per_page = flask.current_app.config['FLASKY_POSTS_PER_PAGE'],
                    error_out = False)

        members = pagination.items

        return flask.render_template('houses/house_profile.html', house = House, 
                tab_variable = tab_variable, pagination = pagination, members = members, 
                count = len(members))

    elif tab_variable == 2:
        return flask.render_template('houses/house_profile.html', house = House, 
                tab_variable = tab_variable)

    elif tab_variable == 3:
        return flask.render_template('houses/house_profile.html', house = House, 
                tab_variable = tab_variable)

    elif tab_variable == 4:
        return flask.render_template('houses/house_profile.html', house = House,
                tab_variable = tab_variable)

    elif tab_variable == 5:
        return flask.render_template('houses/house_profile.html', house = House,
                tab_variable = tab_variable)

    elif tab_variable == 6:
        return flask.render_template('houses/house_profile.html', house = House,
                tab_variable = tab_variable)


@houses.route('/register_house', methods = ["GET", "POST"])
def register_house():

    form = HouseRegistrationForm()
    if form.validate_on_submit():
        house_1 = house(
            house_title = form.house_name.data,
            year_established = form.year_established.data,
            opened_by = form.opened_by.data,
            motto = form.motto.data,
            bed_cover = form.bed_cover.data,
            sister_house = form.sister_house.data,
        )
        db.session.add(house_1)
        db.session.commit()

        flask.flash('%r house registered successfully'%form.house_name.data)
        return flask.redirect(flask.url_for('houses.houses'))

    return flask.render_template('houses/register_house.html', form = form)


@houses.route('/houses', methods = ['GET', 'POST'])
def houses():
    houses = house.query.order_by(house.year_established.desc()).all()

    return flask.render_template('houses/houses.html', houses = houses)

