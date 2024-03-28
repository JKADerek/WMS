from app.extensions import db, bcrypt
from flask_security import UserMixin, RoleMixin
import random
import string

# Association table for the many-to-many relationship between users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

# Association table for the many-to-many relationship between roles and permissions
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    must_reset_password = db.Column(db.Boolean, default=False)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.fs_uniquifier = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def set_random_password(self):
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.password = bcrypt.generate_password_hash(random_password).decode('utf-8')
        self.must_reset_password = True
        return random_password

class AdminSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(120), default="admin@example.com")

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(20), nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    reorder_level = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)
    supplier_contact = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(100))

class InventoryColumnSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column_name = db.Column(db.String(64), unique=True)
    visible = db.Column(db.Boolean, default=True)
