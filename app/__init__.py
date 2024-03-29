from flask import Flask
from flask_uploads import configure_uploads
from logging.handlers import RotatingFileHandler
import logging
import os
from app.config import Config
from app.extensions import db, bcrypt, migrate, mail, photos, security, login_manager  # Make sure login_manager is imported here
from flask_security import SQLAlchemyUserDatastore
# Importing user_datastore directly here is removed to avoid circular import

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)  # Correctly assuming you define login_manager in extensions.py
    migrate.init_app(app, db)
    mail.init_app(app)
    configure_uploads(app, photos)
    
    # Blueprint registration needs to be inside the create_app function
    from app.auth.auth import auth as auth_blueprint
    from app.admin.admin import admin as admin_blueprint
    from app.inventory.inventory import inventory as inventory_blueprint
    from app.main.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')

    # Initialize Flask-Security within app context
    with app.app_context():
        from app.models.models import User, Role
        # Initialize user_datastore inside the app context
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app, user_datastore)

    # Logging setup
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')

    return app
