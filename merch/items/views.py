# items/views.py
import calendar
from flask import render_template, url_for, flash, request, redirect, Blueprint
from merch import db
from merch.models import Item, Category, ItemMonthlyTotal
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
        item.prior_month_total = 0
        item.difference = item.total_qty
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
        old_total = item.total_qty
        new_total = (form.foh_qty.data or 0) + (form.boh_qty.data or 0) + (form.room_300_qty.data or 0)
        now = datetime.now(timezone.utc)
        last_updated = item.date or now

        if (last_updated.year, last_updated.month) != (now.year, now.month):
            prev_year = now.year
            prev_month = now.month - 1
            if prev_month == 0:
                prev_month = 12
                prev_year -= 1
            last_day = calendar.monthrange(prev_year, prev_month)[1]
            month_end = datetime(prev_year, prev_month, last_day, tzinfo=timezone.utc)

            snapshot = ItemMonthlyTotal.query.filter_by(item_id=item.id).first()
            if snapshot is None:
                snapshot = ItemMonthlyTotal(
                    item_id=item.id,
                    month_end=month_end,
                    total_qty=old_total
                )
                db.session.add(snapshot)
            else:
                snapshot.month_end = month_end
                snapshot.total_qty = old_total

            item.prior_month_total = old_total

        item.name = form.name.data
        item.foh_qty = form.foh_qty.data
        item.boh_qty = form.boh_qty.data
        item.room_300_qty = form.room_300_qty.data
        item.item_cost = form.item_cost.data or 0
        item.category_id = form.category_id.data
        prior_total = item.prior_month_total or 0
        item.difference = new_total - prior_total
        # update timestamp to now (UTC)
        item.date = now
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
