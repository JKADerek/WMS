from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from urllib.parse import urlsplit
from app.forms.auth_forms import LoginForm  # Corrected import
from app.models.models import User
from app.extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            # Update starts here
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('main.dashboard')
            # Update ends here
            return redirect(next_page)
        else:
            flash('Invalid email address or password.', 'warning')
    return render_template('auth/login.html', form=form)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect to the login page after logging out
    return redirect(url_for('auth.login'))
