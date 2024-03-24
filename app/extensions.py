from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
photos = UploadSet('photos', IMAGES)
mail = Mail()  # Initialize Flask-Mail

# Further configurations for Flask-Mail, such as setting up SMTP settings, can be done in your Flask app initialization.
