from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()  # Initialize Flask-Migrate
photos = UploadSet('photos', IMAGES)  # Set up Flask-Uploads for image handling

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Flask-Uploads configuration
    app.config['UPLOADED_PHOTOS_DEST'] = 'app/static/img'  # Define where to store uploaded images
    configure_uploads(app, photos)

    # Initialize extensions with the app instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Attach Flask-Migrate to the app and database

    # Import and register blueprints
    from app.auth import auth as auth_blueprint
    from app.inventory import inventory as inventory_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')

    return app
