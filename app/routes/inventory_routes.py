from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from .forms import InventoryForm
from .models import InventoryItem
from . import db, photos

inventory = Blueprint('inventory', __name__)

@inventory.route('/inventory')
def inventory_dashboard():
    items = InventoryItem.query.all()
    return render_template('inventory_dashboard.html', items=items)

@inventory.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
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
        return redirect(url_for('inventory.inventory_dashboard'))
    return render_template('add_inventory_item.html', form=form)
