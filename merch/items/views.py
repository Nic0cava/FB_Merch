# items/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint
from merch import db
from merch.models import Item, Category
from merch.items.forms import AddItemForm, UpdateItemForm, DeleteItemForm

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
            quantity=form.quantity.data,
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
    form = UpdateItemForm()
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
        item.quantity = form.quantity.data
        item.category_id = form.category_id.data
        db.session.commit()
        flash('Item updated', 'success')
        return redirect(url_for('core.index'))

    # on GET pre-fill the form
    if request.method == 'GET':
        form.name.data = item.name
        form.quantity.data = item.quantity
        form.category_id.data = item.category_id

    # flash validation errors after POST
    if request.method == 'POST' and form.errors:
        field, errs = next(iter(form.errors.items()))
        flash(errs[0], 'danger')

    return render_template('update_item.html', form=form, item=item, delete_form=delete_form)
