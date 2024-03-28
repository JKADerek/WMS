from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES
from flask_mail import Mail
from flask_migrate import Migrate


# Initialize Flask extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
photos = UploadSet('photos', IMAGES)
mail = Mail()


# Now, you can initialize Flask-Security in your application factory using:
# security.init_app(app, user_datastore)
