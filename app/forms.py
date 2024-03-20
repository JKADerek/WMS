from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed
from app import photos  # Ensure you've initialized `photos` UploadSet in your __init__.py

class LoginForm(FlaskForm):
    # Keep your existing LoginForm fields

class RegisterForm(FlaskForm):
    # Keep your existing RegisterForm fields

class InventoryForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    quantity_in_stock = StringField('Quantity in Stock', validators=[DataRequired()])
    reorder_level = StringField('Reorder Level', validators=[DataRequired()])
    unit_cost = StringField('Unit Cost', validators=[DataRequired()])
    supplier_name = StringField('Supplier Name', validators=[DataRequired()])
    supplier_contact = StringField('Supplier Contact', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image = FileField('Item Image', validators=[FileAllowed(photos, 'Images only!')])
