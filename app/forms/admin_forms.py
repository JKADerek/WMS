from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    role_id = StringField('Role ID', validators=[DataRequired()])  # You may adjust this based on your needs
    submit = SubmitField('Create User')

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Create Role')

class AssignPermissionsForm(FlaskForm):
    permissions = StringField('Permissions', validators=[DataRequired()])  # You may adjust this based on your needs
    submit = SubmitField('Assign Permissions')

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
                visible_columns.append(field.name[:-8])  # remove '_visible' suffix
        return visible_columns

    def set_column_visibility(self, column_name, visibility):
        setattr(self, f"{column_name}_visible", visibility)
