from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Other User fields...

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Other InventoryItem fields...
