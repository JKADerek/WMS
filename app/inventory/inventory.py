from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_security import login_required, roles_accepted
from app.models.models import InventoryItem
from app.forms.inventory_forms import InventoryForm
from app.extensions import db, photos
from werkzeug.utils import secure_filename
from flask_uploads import UploadNotAllowed

inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory.route('/inventory_dashboard')
@login_required
@roles_accepted('Admin', 'InventoryManager')
def inventory_dashboard():
    inventory_items = InventoryItem.query.all()
    visible_columns = [
        ('Name', 'name'),
        ('Quantity In Stock', 'quantity_in_stock'),
        ('Unit Cost', 'unit_cost'),
        ('Supplier Name', 'supplier_name')
    ]
    return render_template('inventory/inventory_dashboard.html', inventory_items=inventory_items, visible_columns=visible_columns)


@inventory.route('/add_inventory_item', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'InventoryManager')
def add_inventory_item():
    form = InventoryForm()
    if form.validate_on_submit():
        filename = None  # Initialize filename to None
        if form.image.data:
            try:
                filename = photos.save(form.image.data, name=secure_filename(form.image.data.filename))
            except UploadNotAllowed:
                flash('Upload not allowed', 'error')
                return redirect(url_for('inventory.add_inventory_item'))  # Stay on the form page if upload fails

        # Create a new InventoryItem instance
        new_item = InventoryItem(
            item_name=form.item_name.data,
            sku=form.sku.data,
            quantity_in_stock=form.quantity_in_stock.data,
            reorder_level=form.reorder_level.data,
            unit_cost=form.unit_cost.data,
            supplier_name=form.supplier_name.data,
            supplier_contact=form.supplier_contact.data,
            location=form.location.data,
            image_filename=filename  # This will be None if no file was selected/upload failed
        )
        
        # Add the new item to the database session and commit
        db.session.add(new_item)
        db.session.commit()
        flash('New inventory item added successfully!', 'success')
        
        # Redirect to the inventory dashboard after successful addition
        return redirect(url_for('inventory.inventory_dashboard'))
    
    # Render the add_inventory_item template with the form
    return render_template('inventory/add_inventory_item.html', form=form)


@inventory.route('/edit_inventory_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'InventoryManager')
def edit_inventory_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    form = InventoryForm(obj=item)
    if form.validate_on_submit():
        # Update item details here...

        if form.image.data:
            filename = photos.save(form.image.data, name=secure_filename(form.image.data.filename))
            item.image_filename = filename
        db.session.commit()
        flash('Inventory item updated successfully.', 'success')
        return redirect(url_for('inventory.inventory_dashboard'))

    # Update the template path to 'inventory/edit_inventory_item.html'
    return render_template('inventory/edit_inventory_item.html', form=form, item=item)

@inventory.route('/delete_inventory_item/<int:item_id>', methods=['POST'])
@login_required
@roles_accepted('Admin', 'InventoryManager')
def delete_inventory_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Inventory item deleted successfully.', 'success')
    return redirect(url_for('inventory.inventory_dashboard'))

@inventory.route('/reports/generate')
@login_required
@roles_accepted('Admin', 'InventoryManager')
def generate_inventory_report():
    items = InventoryItem.query.all()
    # Update the template path to 'inventory/reports/generate_inventory_report.html'
    return render_template('inventory/reports/generate_inventory_report.html', items=items)
