import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '-'
    UPLOAD_FOLDER = 'app/static/usersimg'


    # Mail Settings
    SECURITY_PASSWORD_SALT ="-"
    MAIL_SERVER = "smtp.mail.ru"
    MAIL_PORT = 2525
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = "-"
    MAIL_PASSWORD = "-"
