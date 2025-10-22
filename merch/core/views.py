# merch/core/views.py
from flask import render_template, request, Blueprint
from merch.models import Category, Item
from collections import defaultdict


core = Blueprint('core', __name__)

@core.route('/')
def index():
    q = request.args.get('q', '').strip()
    q_lower = q.lower() if q else ''

    # load categories (no joinedload because items may be dynamic)
    categories = Category.query.order_by(Category.name).all()
    cat_ids = [c.id for c in categories]

    # load all items for those categories in a single query, then group
    items = Item.query.filter(Item.category_id.in_(cat_ids)).order_by(Item.name).all() if cat_ids else []
    items_by_cat = defaultdict(list)
    for it in items:
        items_by_cat[it.category_id].append(it)

    for cat in categories:
        items = items_by_cat.get(cat.id, []) or []
        if q_lower:
            filtered = [i for i in items if q_lower in (i.name or '').lower()]
            cat.sorted_items = sorted(filtered, key=lambda i: (i.name or '').lower())
        else:
            cat.sorted_items = sorted(items, key=lambda i: (i.name or '').lower())

    # when searching, drop categories that have no matching items
    if q_lower:
        categories = [c for c in categories if c.sorted_items]


    return render_template('index.html', categories=categories)