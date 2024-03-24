from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms.admin_forms import CreateUserForm, RoleForm, AssignPermissionsForm, InventoryColumnForm  
from app.models.models import User, Role, Permission, InventoryColumnSettings, AdminSettings
from app.extensions import db, mail
from flask_mail import Message
from app import mail

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
def dashboard():
    # Ensure only users with the ability to manage users can view the admin dashboard
    if not current_user.can(Permission.MANAGE_USERS):
        flash('Access denied: Insufficient permissions', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin/dashboard.html')

@admin.route('/users')
@login_required
def manage_users():
    if not current_user.can(Permission.MANAGE_USERS):
        flash('Access denied: Insufficient permissions', 'danger')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        # Create the user and generate a random password
        user = User(email=form.email.data)
        random_password = user.set_random_password()
        user.role_id = form.role_id.data
        db.session.add(user)
        db.session.commit()
        
        # Fetch the sender email from AdminSettings or use a default
        settings = AdminSettings.query.first()
        sender_email = settings.sender_email if settings else "default_sender@example.com"
        
        # Send email with the random password
        try:
            msg = Message("Your Account Information",
                          sender=sender_email,
                          recipients=[user.email])
            msg.body = f"""
            An account has been created for you. Your temporary password is: {random_password}
            Please log in and reset your password immediately.
            """
            mail.send(msg)
            flash('User created successfully and notified via email.', 'success')
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'danger')
        
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/create_user.html', form=form)

    
@admin.route('/roles')
@login_required
def manage_roles():
    if not current_user.can(Permission.MANAGE_USERS):
        flash('Access denied: Insufficient permissions', 'danger')
        return redirect(url_for('main.index'))
    roles = Role.query.all()
    return render_template('admin/manage_roles.html', roles=roles)

@admin.route('/create_role', methods=['GET', 'POST'])
@login_required
def create_role():
    if not current_user.can(Permission.MANAGE_USERS):
        flash('Access denied: Insufficient permissions', 'danger')
        return redirect(url_for('main.index'))
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data)
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully.', 'success')
        return redirect(url_for('admin.manage_roles'))
    return render_template('admin/create_role.html', form=form)

@admin.route('/assign_permissions/<int:role_id>', methods=['GET', 'POST'])
@login_required
def assign_permissions(role_id):
    if not current_user.can(Permission.MANAGE_USERS):
        flash('Access denied: Insufficient permissions', 'danger')
        return redirect(url_for('main.index'))
    role = Role.query.get_or_404(role_id)
    form = AssignPermissionsForm(obj=role)
    if form.validate_on_submit():
        # Assuming you have a method in your Role model to handle permission updates
        role.update_permissions(form.permissions.data)
        db.session.commit()
        flash('Permissions updated successfully.', 'success')
        return redirect(url_for('admin.manage_roles'))
    return render_template('admin/assign_permissions.html', form=form, role=role)

@admin.route('/inventory/columns')
@login_required
def manage_inventory_columns():
    if not current_user.can(Permission.MANAGE_INVENTORY):
        flash('Access denied: Insufficient permissions.', 'danger')
        return redirect(url_for('admin.dashboard'))
    columns = InventoryColumnSettings.query.all()
    return render_template('admin/manage_inventory_columns.html', columns=columns)

@admin.route('/manage_inventory_columns', methods=['GET', 'POST'])
@login_required
def update_inventory_columns():
    form = InventoryColumnForm()
    if form.validate_on_submit():
        # Example logic to update column settings based on form data
        for field in form:
            if 'column_' in field.name:  # Assuming your form fields for columns start with 'column_'
                column_name = field.name.replace('column_', '')
                setting = InventoryColumnSettings.query.filter_by(column_name=column_name).first()
                if setting:
                    setting.visible = field.data
        db.session.commit()
        flash('Inventory dashboard columns updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/admin.html', form=form)

@admin.route('/update_email_settings', methods=['POST'])
@login_required
def update_email_settings():
    if not current_user.can(Permission.MANAGE_USERS):  # Adjust according to your permissions system
        flash('Access denied: Insufficient permissions.', 'danger')
        return redirect(url_for('admin.dashboard'))

    new_sender_email = request.form.get('sender_email')
    if new_sender_email:
        settings = AdminSettings.query.first()  # Assuming only one settings row
        settings.sender_email = new_sender_email
        db.session.commit()
        flash('Sender email address updated successfully.', 'success')
    else:
        flash('Invalid email address.', 'danger')
    return redirect(url_for('admin.dashboard'))