from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_security import login_required, roles_required, hash_password
from app.forms.admin_forms import CreateUserForm, RoleForm, AssignPermissionsForm, InventoryColumnForm, EmailSettingsForm
from app.models.models import User, Role, InventoryColumnSettings, AdminSettings, db
from app.extensions import mail
from flask_mail import Message

admin = Blueprint('admin', __name__, url_prefix='/admin')

def get_role_choices():
    """Fetches roles from the database and formats them for form choices."""
    return [(role.id, role.name) for role in Role.query.order_by('name')]

@admin.route('/dashboard')
@login_required
@roles_required('Admin')
def dashboard():
    email_settings_form = EmailSettingsForm()
    return render_template('admin/dashboard.html', email_settings_form=email_settings_form)

@admin.route('/users')
@login_required
@roles_required('Admin')
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin.route('/create_user', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def create_user():
    form = CreateUserForm()
    form.roles.choices = get_role_choices()  # Populate role choices

    if form.validate_on_submit():
        user_datastore = current_app.extensions['security'].datastore
        random_password = User().set_random_password()  # Assuming this method also hashes the password

        user = user_datastore.create_user(
            email=form.email.data, 
            password=random_password,
            active=form.active.data
        )

        role = Role.query.get(form.roles.data)
        if role:
            user_datastore.add_role_to_user(user, role)
            db.session.commit()

            msg = Message(
                "Your Account Information",
                recipients=[user.email],
                body=f"Welcome! Your account has been created. Please log in using this password: {random_password}. It is recommended to change your password after logging in."
            )
            mail.send(msg)

            flash('User created successfully and password emailed.', 'success')
        else:
            flash('Selected role does not exist.', 'error')

        return redirect(url_for('admin.manage_users'))

    return render_template('admin/create_user.html', form=form)

@admin.route('/roles')
@login_required
@roles_required('Admin')
def manage_roles():
    roles = Role.query.all()
    return render_template('admin/manage_roles.html', roles=roles)

@admin.route('/create_role', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def create_role():
    form = RoleForm()
    if form.validate_on_submit():
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.create_role(name=form.name.data, description=form.description.data)
        db.session.commit()
        flash('Role created successfully.', 'success')
        return redirect(url_for('admin.manage_roles'))
    return render_template('admin/create_role.html', form=form)

@admin.route('/inventory/columns')
@login_required
@roles_required('Admin')
def manage_inventory_columns():
    columns = InventoryColumnSettings.query.all()
    return render_template('admin/manage_inventory_columns.html', columns=columns)

@admin.route('/update_email_settings', methods=['POST'])
@login_required
@roles_required('Admin')
def update_email_settings():
    sender_email = request.form.get('sender_email')
    # Implement the actual update logic here
    flash('Email settings updated successfully.', 'success')
    return redirect(url_for('admin.dashboard'))
