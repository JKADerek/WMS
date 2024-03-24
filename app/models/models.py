from app.extensions import db
from flask_login import UserMixin

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.relationship('Permission', secondary='role_permissions', backref=db.backref('roles', lazy='dynamic'))

class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Ensure this password is hashed appropriately
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
    must_reset_password = db.Column(db.Boolean, default=False)
    
    # Method to set a random password and flag for reset
    def set_random_password(self):
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.password_hash = generate_password_hash(random_password)
        self.must_reset_password = True
        return random_password

    def can(self, permission_name):
        return any(permission.name == permission_name for permission in self.role.permissions)

    def add_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if role:
            self.role = role
            return True
        return False

class AdminSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(120), default="admin@example.com")  # Default sender email


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
    image_filename = db.Column(db.String(100))  # Optional: handle image upload separately
   
    def __repr__(self):
        return f'<InventoryItem {self.item_name}>'

class InventoryColumnSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column_name = db.Column(db.String(64), unique=True)
    visible = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<InventoryColumnSettings {self.column_name}>'
