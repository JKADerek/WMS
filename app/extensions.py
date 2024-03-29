# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
photos = UploadSet('photos', IMAGES)
mail = Mail()
security = Security()
