import os

class Config:
    # Basic configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_fallback_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587  # or 465 for SSL
    MAIL_USE_TLS = True  # or False if you are using SSL with MAIL_PORT = 465
    MAIL_USE_SSL = False  # or True if you are using SSL with MAIL_PORT = 465
    MAIL_USERNAME = 'derek@jkawelldrilling.com'  # Your full Gmail address
    MAIL_PASSWORD = 'obca bnta bisx fyci'  # Your Gmail password or App password
    MAIL_DEFAULT_SENDER = 'derek@jkawelldrilling.com'  # Your full Gmail address


      # Flask-Security template configurations
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'
    SECURITY_CHANGE_PASSWORD_TEMPLATE = 'security/change_password.html'
    SECURITY_FORGOT_PASSWORD_TEMPLATE = 'security/forgot_password.html'
    SECURITY_SEND_CONFIRMATION_TEMPLATE = 'security/send_confirmation.html'


    # Flask-Security configuration
    SECURITY_PASSWORD_SALT = 'some_random_salt'
    SECURITY_REGISTERABLE = True  # Enable user registration
    SECURITY_CONFIRMABLE = True  # Enable email confirmation
    SECURITY_RECOVERABLE = True  # Enable password recovery

    # Flask-Uploads configuration
    UPLOADED_PHOTOS_DEST = os.environ.get('UPLOADED_PHOTOS_DEST') or 'app/static/img'

    # Logging configuration
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
