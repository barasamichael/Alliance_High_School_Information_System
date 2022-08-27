import flask
import flask_sqlalchemy
import flask_bootstrap
import flask_mail
import flask_moment

from flask_login import LoginManager

from config import config

mail = flask_mail.Mail()
db = flask_sqlalchemy.SQLAlchemy()
moment = flask_moment.Moment()
bootstrap = flask_bootstrap.Bootstrap()

def create_app(config_name):
    """
    Application initialization.
    Takes as an argument one of the configuration classes defined in config.py
    """

    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    mail.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .houses import houses as houses_blueprint
    app.register_blueprint(houses_blueprint, url_prefix = "/houses")

    from .students import students as students_blueprint
    app.register_blueprint(students_blueprint, url_prefix = "/students")

    from .clubs import clubs as clubs_blueprint
    app.register_blueprint(clubs_blueprint, url_prefix = "/clubs")

    from .obc import obc as obc_blueprint
    app.register_blueprint(obc_blueprint, url_prefix = "/obc")

    from .sanatorium import sanatorium as sanatorium_blueprint
    app.register_blueprint(sanatorium_blueprint, url_prefix = "/sanatorium")

    from .academics import academics  as academics_blueprint
    app.register_blueprint(academics_blueprint, url_prefix = "/academics")

    from .departments import departments  as departments_blueprint
    app.register_blueprint(departments_blueprint, url_prefix = "/departments")

    from .library import library as library_blueprint
    app.register_blueprint(library_blueprint, url_prefix = "/library")

    from .sports import sports as sports_blueprint
    app.register_blueprint(sports_blueprint, url_prefix = "/sports")

    from .administration import administration as administration_blueprint
    app.register_blueprint(administration_blueprint, url_prefix = "/administration")

    from .leadership import leadership as leadership_blueprint
    app.register_blueprint(leadership_blueprint, url_prefix = "/leadership")

    return app
