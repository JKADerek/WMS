# file: app/inventory/inventory.py
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.models import InventoryItem, Permission
from app.forms.inventory_forms import InventoryForm
from app.extensions import db, photos
from werkzeug.utils import secure_filename

inventory = Blueprint('inventory', __name__)

@inventory.route('/inventory/inventory_dashboard')
@login_required
def inventory_dashboard():
    if not current_user.can(Permission.VIEW_INVENTORY):
        flash('Access denied: Insufficient permissions.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Check if the user has permission to generate reports
    can_generate_reports = current_user.can('generate_reports')
    
    items = InventoryItem.query.all()
    # Pass the 'can_generate_reports' flag to the template
    return render_template('inventory_dashboard.html', items=items, can_generate_reports=can_generate_reports)

@inventory.route('/inventory/add_inventory_item', methods=['GET', 'POST'])
@login_required
def add_inventory_item():
    if not current_user.can(Permission.MANAGE_INVENTORY):
        flash('Access denied: Insufficient permissions.', 'danger')
        return redirect(url_for('inventory.inventory_dashboard'))
    
    form = InventoryForm()
    if form.validate_on_submit():
        filename = photos.save(form.image.data, name=secure_filename(form.image.data.filename))
        new_item = InventoryItem(
            item_name=form.item_name.data,
            sku=form.sku.data,
            quantity_in_stock=form.quantity_in_stock.data,
            reorder_level=form.reorder_level.data,
            unit_cost=form.unit_cost.data,
            supplier_name=form.supplier_name.data,
            supplier_contact=form.supplier_contact.data,
            location=form.location.data,
            image_filename=filename  # Ensure your model has this field
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Inventory item added successfully.', 'success')
        return redirect(url_for('inventory.inventory_dashboard'))
    return render_template('add_inventory_item.html', form=form)

@inventory.route('/inventory/edit_inventory_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_inventory_item(item_id):
    if not current_user.can(Permission.MANAGE_INVENTORY):
        flash('Access denied: Insufficient permissions.', 'danger')
        return redirect(url_for('inventory.inventory_dashboard'))
    
    item = InventoryItem.query.get_or_404(item_id)
    form = InventoryForm(obj=item)
    if form.validate_on_submit():
        item.item_name = form.item_name.data
        item.sku = form.sku.data
        item.quantity_in_stock = form.quantity_in_stock.data
        item.reorder_level = form.reorder_level.data
        item.unit_cost = form.unit_cost.data
        item.supplier_name = form.supplier_name.data
        item.supplier_contact = form.supplier_contact.data
        item.location = form.location.data
        # Handle image updates if necessary
        if form.image.data:
            filename = photos.save(form.image.data, name=secure_filename(form.image.data.filename))
            item.image_filename = filename
        db.session.commit()
        flash('Inventory item updated successfully.', 'success')
        return redirect(url_for('inventory.inventory_dashboard'))
    form.process(obj=item)
    return render_template('edit_inventory_item.html', form=form, item_id=item_id)

@inventory.route('/inventory/delete_inventory_item/<int:item_id>', methods=['POST'])
@login_required
def delete_inventory_item(item_id):
    if not current_user.can(Permission.MANAGE_INVENTORY):
        flash('Access denied: Insufficient permissions.', 'danger')
        return redirect(url_for('inventory.inventory_dashboard'))
    
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Inventory item deleted successfully.', 'success')
    return redirect(url_for('inventory.inventory_dashboard'))

@inventory.route('/reports/generate')
@login_required
def generate_inventory_report():
    if not current_user.can('generate_reports'):
        flash('Access denied: Insufficient permissions to generate inventory reports.', 'danger')
        return redirect(url_for('inventory.inventory_dashboard'))

    # Query the database for inventory items
    items = InventoryItem.query.all()

    # Pass the items to the template for display
    return render_template('inventory/reports/generate_inventory_report.html', items=items)