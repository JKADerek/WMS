from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_security.utils import hash_password
from flask_security import login_required, roles_required, current_user, SQLAlchemyUserDatastore
from app.forms.admin_forms import CreateUserForm, RoleForm, AssignPermissionsForm, InventoryColumnForm, EmailSettingsForm
from app.models.models import User, Role, InventoryColumnSettings, AdminSettings
from app.extensions import db, mail
from flask_mail import Message

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
@roles_required('Admin')  # Example of using Flask-Security's role requirement
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

    if form.validate_on_submit():
        # Instantiate a new User object
        user = User(email=form.email.data, active=form.active.data)
        
        # Generate a random password for the user instance
        random_password = user.set_random_password()
        
        # Create a new user with the random password
        user_datastore.create_user(
            email=user.email, 
            password=random_password,  # Flask-Security will handle the password hashing
            active=user.active
        )

        # Find and assign the selected role to the user
        role = user_datastore.find_role(form.roles.data)  # Assuming 'roles' contains the role name
        user_datastore.add_role_to_user(user, role)

        # Commit changes to the database
        db.session.commit()

        # Email the random password to the user
        msg = Message(
            "Your Account Information",
            recipients=[user.email],
            body=f"Welcome! Your account has been created. Please log in using this password: {random_password}. It is recommended to change your password after logging in."
        )
        mail.send(msg)

        flash('User created successfully and password emailed.', 'success')
        return redirect(url_for('admin.manage_users'))

    # Pre-populate the roles field choices
    form.roles.choices = [(role.id, role.name) for role in Role.query.order_by('name')]

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
        from app.extensions import user_datastore
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
    # Example of retrieving form data
    sender_email = request.form.get('sender_email')
    
    # Placeholder: Update your email settings here
    # This could involve updating application configuration, a database entry, or another storage mechanism
    # For example:
    # admin_settings = AdminSettings.query.first()
    # admin_settings.sender_email = sender_email
    # db.session.commit()
    
    flash('Email settings updated successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

# Additional routes as needed

