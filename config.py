import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
            'bringing bush to your device'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '587')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true')\
            .lower() in ['True', 'on', 1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_ADMIN_EMAIL = 'ourdigitaltimes@gmail.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Alliance High School]'
    FLASKY_MAIL_SENDER = 'Alliance High School Admin < ourdigitaltimes@gmail.com >'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGANISATION_NAME = 'Alliance High School'
    FLASKY_RECORDS_PER_PAGE = 25
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_ITEMS_PER_PAGE = 10
    UPLOAD_PATH = os.path.join(basedir + '/app/static/clubs')
    CLUB_EVENT_UPLOAD_PATH = os.path.join(basedir + '/app/static/clubs/events')
    EVENTS_UPLOAD_PATH = os.path.join(basedir + '/app/static/obc')
    LIBRARY_UPLOAD_PATH = os.path.join(basedir + '/app/static/library')
    SPORTS_UPLOAD_PATH = os.path.join(basedir + '/app/static/sports')
    HOUSES_UPLOAD_PATH = os.path.join(basedir + '/app/static/houses')

    UPLOAD_EXTENSIONS = ['.jpg', '.gif', '.jpeg', '.png']


@staticmethod
def init_app(app):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
            or 'sqlite:///' + os.path.join(basedir, 'data-dev-sqlite')
    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
            or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'production' : ProductionConfig,
        'default' : DevelopmentConfig
        }





