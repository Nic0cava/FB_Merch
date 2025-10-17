# merch/core/views.py
from flask import render_template, request, Blueprint
from merch.models import Category, Item


core = Blueprint('core', __name__)

@core.route('/')
def index():
    # load all categories ordered by name
    categories = Category.query.order_by(Category.name).all()

    # attach an alphabetically-ordered items list to each category
    for cat in categories:
        cat.sorted_items = Item.query.filter_by(category_id=cat.id).order_by(Item.name).all()

    return render_template('index.html', categories=categories)