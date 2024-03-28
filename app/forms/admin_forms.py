from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models.models import Role  # Ensure this import is correct based on your application structure
from flask_security.forms import Required

def get_role_choices():
    return [(role.id, role.name) for role in Role.query.order_by('name')]

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    roles = SelectField('Role', choices=[], coerce=int)  # We'll populate this in the view
    active = BooleanField('Active', default=True)
    submit = SubmitField('Create User')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.roles.choices = get_role_choices()  # Populate the choices

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(max=80)])
    description = StringField('Description', validators=[Length(max=255)])
    submit = SubmitField('Create Role')

class AssignPermissionsForm(FlaskForm):
    # Assuming permissions are managed by name within Roles
    role_id = SelectField('Role', choices=[], coerce=int)
    permission_name = StringField('Permission Name', validators=[DataRequired()])
    submit = SubmitField('Assign Permission')

    def __init__(self, *args, **kwargs):
        super(AssignPermissionsForm, self).__init__(*args, **kwargs)
        self.role_id.choices = get_role_choices()

class InventoryColumnForm(FlaskForm):
    item_name_visible = BooleanField('Item Name')
    sku_visible = BooleanField('SKU')
    quantity_in_stock_visible = BooleanField('Quantity in Stock')
    reorder_level_visible = BooleanField('Reorder Level')
    unit_cost_visible = BooleanField('Unit Cost')
    supplier_name_visible = BooleanField('Supplier Name')
    supplier_contact_visible = BooleanField('Supplier Contact')
    location_visible = BooleanField('Location')
    image_visible = BooleanField('Item Image')
    submit = SubmitField('Save')

    def get_visible_columns(self):
        visible_columns = []
        for field in self:
            if field.name.endswith('_visible') and field.data:
                visible_columns.append(field.name[:-8])  # Remove '_visible' suffix
        return visible_columns

    def set_column_visibility(self, column_name, visibility):
        setattr(self, f"{column_name}_visible", visibility)

class EmailSettingsForm(FlaskForm):
    sender_email = StringField('Sender Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Settings')