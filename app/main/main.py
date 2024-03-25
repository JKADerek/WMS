from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Permission
from app.extensions import db

main = Blueprint('main', __name__)

# file: app/main/main.py

@main.route('/')
def index():
    if current_user.is_authenticated:
        # Redirect to the inventory dashboard if the user is logged in
        return redirect(url_for('main.dashboard'))
    # Otherwise, redirect to the login page
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Check if the user has the 'view_dashboard' permission
    if not current_user.can('view_dashboard'):
        flash('Access denied: Insufficient permissions to view the dashboard.', 'danger')
        return redirect(url_for('main.index'))
    
    # Proceed to render the dashboard if the user has permission
    return render_template('dashboard.html')