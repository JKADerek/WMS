# app/forms/inventory_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed
from app.extensions import photos  # Adjust this import based on your actual extensions.py location

class InventoryForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    sku = StringField('SKU', validators=[DataRequired(), Length(max=20)])
    quantity_in_stock = IntegerField('Quantity in Stock', validators=[DataRequired(), NumberRange(min=0)])
    reorder_level = IntegerField('Reorder Level', validators=[DataRequired(), NumberRange(min=0)])
    unit_cost = FloatField('Unit Cost', validators=[DataRequired(), NumberRange(min=0.01)])
    supplier_name = StringField('Supplier Name', validators=[DataRequired(), Length(max=100)])
    supplier_contact = StringField('Supplier Contact', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    image = FileField('Item Image', validators=[FileAllowed(photos, 'Images only!')])
    submit = SubmitField('Submit')

