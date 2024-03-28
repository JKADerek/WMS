from flask import Blueprint, redirect, url_for
from flask_security import current_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('security.login'))
