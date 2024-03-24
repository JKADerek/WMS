from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Permission
from app.extensions import db

main = Blueprint('main', __name__)

# file: app/main/routes.py
from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        # Redirect to the inventory dashboard if the user is logged in
        return redirect(url_for('inventory.inventory_dashboard'))
    # Otherwise, redirect to the login page
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Dashboard route, accessible to any authenticated user
    # If you have different dashboards, you can redirect to a specific one here
    return render_template('dashboard.html')
