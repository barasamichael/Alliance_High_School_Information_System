import flask, os, imghdr
from . import administration
from .. import db

from werkzeug.utils import secure_filename

from .forms import (UpdateProfileImageForm)

from ..models import (student)

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@administration.route('/')
@administration.route('/homepage')
def homepage():
    return flask.render_template('administration/admin_homepage.html')
