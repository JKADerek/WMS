from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Add any other fields for User

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(20), nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    reorder_level = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    supplier_contact = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True)  # Added to store the image filename

    def __repr__(self):
        return f'<InventoryItem {self.item_name}>'
