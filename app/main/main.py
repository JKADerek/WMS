from flask import Blueprint, render_template, redirect, url_for, flash
from flask_security import login_required, roles_required, roles_accepted, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        # Redirect to the inventory dashboard if the user is logged in
        return redirect(url_for('main.dashboard'))
    # Otherwise, redirect to Flask-Security's login view
    return redirect(url_for('security.login'))  # Updated to use Flask-Security's default login view

@main.route('/dashboard')
@login_required  # Ensures that the user must be authenticated to view the dashboard
@roles_accepted('Admin', 'User')  # Assuming 'Admin' and 'User' roles have permission to view dashboard
def dashboard():
    # The check for specific permissions can be done here if needed, 
    # but @roles_accepted simplifies access control based on roles

    # Proceed to render the dashboard
    return render_template('dashboard.html')
