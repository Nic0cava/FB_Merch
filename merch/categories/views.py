# categories/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from merch import db
from merch.models import Category, Item
from merch.categories.forms import AddCategoryForm, UpdateCategoryForm

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
    # load the Category instance (404 if not found)
    cat = Category.query.get_or_404(category_id)

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

    return render_template('update_category.html', form=form, category=cat)