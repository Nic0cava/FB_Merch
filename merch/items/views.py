# items/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint
from merch import db
from merch.models import Item, Category
from merch.items.forms import AddItemForm, UpdateItemForm, DeleteItemForm
from datetime import datetime, timezone

items = Blueprint('items', __name__)


# Add Item
@items.route('/additem', methods=['GET','POST'])
def add_item():
    form = AddItemForm()

    # populate category choices each request
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]


    if form.validate_on_submit():
        item = Item(
            name=form.name.data,
            foh_qty=form.foh_qty.data,
            boh_qty=form.boh_qty.data,
            room_300_qty=form.room_300_qty.data,
            item_cost=form.item_cost.data or 0,
            category_id=form.category_id.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Item added', 'success')
        return redirect(url_for('core.index'))
    
    # if POST and validation failed, flash first error (optional)
    if request.method == 'POST' and form.errors:
        # flash first field error
        field, errs = next(iter(form.errors.items()))
        flash(errs[0], 'danger')

    return render_template('add_item.html', form=form)

# Update Item
@items.route('/updateitem/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    # pass original_name so the validator allows unchanged names
    form = UpdateItemForm(original_name=item.name)
    delete_form = DeleteItemForm()

    # populate category choices each request
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    # Handle delete request first (button named "delete" in template)
    if request.method == 'POST' and 'delete' in request.form:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted', 'success')
        return redirect(url_for('core.index'))

    # Normal Update Flow
    if form.validate_on_submit():
        item.name = form.name.data
        item.foh_qty = form.foh_qty.data
        item.boh_qty = form.boh_qty.data
        item.room_300_qty = form.room_300_qty.data
        item.item_cost = form.item_cost.data or 0
        item.category_id = form.category_id.data
        # update timestamp to now (UTC)
        item.date = datetime.now(timezone.utc)
        db.session.commit()
        flash('Item updated', 'success')
        return redirect(url_for('core.index'))

    # on GET pre-fill the form
    if request.method == 'GET':
        form.name.data = item.name
        form.foh_qty.data = item.foh_qty
        form.boh_qty.data = item.boh_qty
        form.room_300_qty.data = item.room_300_qty
        form.item_cost.data = item.item_cost
        form.category_id.data = item.category_id

    # flash validation errors after POST
    if request.method == 'POST' and form.errors:
        field, errs = next(iter(form.errors.items()))
        flash(errs[0], 'danger')

    return render_template('update_item.html', form=form, item=item, delete_form=delete_form)
