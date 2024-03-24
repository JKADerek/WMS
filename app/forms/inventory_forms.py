# app/forms/inventory_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class InventoryForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    sku = StringField('SKU', validators=[DataRequired(), Length(max=20)])
    quantity_in_stock = StringField('Quantity in Stock', validators=[DataRequired()])
    reorder_level = StringField('Reorder Level', validators=[DataRequired()])
    unit_cost = StringField('Unit Cost', validators=[DataRequired()])
    supplier_name = StringField('Supplier Name', validators=[DataRequired(), Length(max=100)])
    supplier_contact = StringField('Supplier Contact', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    image = FileField('Item Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')
