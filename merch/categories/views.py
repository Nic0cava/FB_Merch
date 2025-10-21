# categories/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from merch import db
from merch.models import Category, Item
from merch.categories.forms import AddCategoryForm, UpdateCategoryForm, DeleteCategoryForm

category = Blueprint('category',__name__)

# AddCategory
@category.route("/addcategory",methods=['GET','POST'])
def add_category():
    form = AddCategoryForm()

    if form.validate_on_submit():
        category = Category(name=form.name.data)

        db.session.add(category)
        db.session.commit()
        flash('New Category Successfully Added!') #! Update this flash later
        return redirect(url_for('core.index'))
    
    # flash validation errors after POST
    if request.method == 'POST' and form.name.errors:
        flash(form.name.errors[0], 'danger')
    
    return render_template('add_category.html',form=form)
    

# UpdateCategory
@category.route('/updatecategory/<int:category_id>', methods=['GET','POST'])
def update_category(category_id):
    form = UpdateCategoryForm()
    delete_form = DeleteCategoryForm()
    # load the Category instance (404 if not found)
    cat = Category.query.get_or_404(category_id)

    # Handle delete request first (button named "delete" in template)
    if request.method == 'POST' and 'delete' in request.form:
        # prevent deletion if category still has items
        # cat.items is a dynamic query in your models, so count() issues a COUNT SQL
        if cat.items.count() == 0:
            db.session.delete(cat)
            db.session.commit()
            flash('Category deleted', 'success')
            return redirect(url_for('core.index'))
        else:
            flash('Cannot delete category while it contains items. Remove or move items first.', 'danger')
            return redirect(url_for('category.update_category', category_id=category_id))

    # Normal Update Flow
    if form.validate_on_submit():
        cat.name = form.name.data
        db.session.commit()
        flash('Category Name Updated!')
        return redirect(url_for('core.index'))

    elif request.method == 'GET':
        form.name.data = cat.name

    # flash validation errors after POST
    if request.method == 'POST' and form.name.errors:
        flash(form.name.errors[0], 'danger')

    return render_template('update_category.html', form=form, category=cat, delete_form=delete_form)