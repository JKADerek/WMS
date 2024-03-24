from flask import Flask, request, Blueprint
from app.config import Config
# Import initialized extensions
from .extensions import db, bcrypt, login_manager, migrate, mail, photos, configure_uploads
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Additional specific configuration if needed
    app.config['UPLOADED_PHOTOS_DEST'] = 'app/static/img'

    # Initialize extensions with the app instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    configure_uploads(app, photos)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from .models.models import User  # Adjust the import path as needed
        return User.query.get(int(user_id))

    # Import and register blueprints
    from app.auth.auth import auth as auth_blueprint
    from app.admin.admin import admin as admin_blueprint
    from app.inventory.inventory import inventory as inventory_blueprint
    from app.main.main import main as main_blueprint
    app.register_blueprint(main_blueprint)  # No URL prefix, to simplify routes like the dashboard
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')

    @app.after_request
    def set_samesite_cookies(response):
        # Your secure cookie settings
        return response

    return app
