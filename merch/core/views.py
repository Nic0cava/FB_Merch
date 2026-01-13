# merch/core/views.py
from io import BytesIO
import re
from flask import render_template, request, Blueprint, send_file
from merch.models import Category, Item
from collections import defaultdict
from openpyxl import Workbook


core = Blueprint('core', __name__)

@core.route('/')
def index():
    q = request.args.get('q', '').strip()
    q_lower = q.lower() if q else ''

    # treat these as "out of stock" searches
    OUT_TOKENS = {'status:out', 'out of stock', 'outofstock', 'oos', 'out', 'stock:0', 'qty:0'}

    is_out_search = q_lower in OUT_TOKENS


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
        if is_out_search:
            filtered = [i for i in items if (i.total_qty or 0) == 0]
            cat.sorted_items = sorted(filtered, key=lambda i: (i.name or '').lower())
        elif q_lower:
            filtered = [i for i in items if q_lower in (i.name or '').lower()]
            cat.sorted_items = sorted(filtered, key=lambda i: (i.name or '').lower())
        else:
            cat.sorted_items = sorted(items, key=lambda i: (i.name or '').lower())


    # when searching, drop categories that have no matching items
    if q_lower:
        categories = [c for c in categories if c.sorted_items]


    return render_template('index.html', categories=categories)


@core.route('/export/items.xlsx')
def export_items():
    category_id = request.args.get('category_id', type=int)
    category = None
    if category_id:
        category = Category.query.get_or_404(category_id)

    query = (Item.query
             .join(Category, Item.category_id == Category.id)
             .order_by(Category.name, Item.name))
    if category:
        query = query.filter(Item.category_id == category.id)
    items = query.all()

    wb = Workbook()
    ws = wb.active
    ws.title = (category.name[:31] if category else 'Items')
    ws.append([
        'Category',
        'Item',
        'FOH',
        'BOH',
        'R300',
        'Total Qty',
        'Item Cost',
        'Total Cost',
        'Updated',
    ])

    for item in items:
        ws.append([
            item.category.name if item.category else '',
            item.name,
            item.foh_qty,
            item.boh_qty,
            item.room_300_qty,
            item.total_qty,
            item.item_cost,
            item.total_cost,
            item.date.strftime('%Y-%m-%d') if item.date else '',
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = 'merch_items.xlsx'
    if category:
        safe_name = re.sub(r'[^A-Za-z0-9_-]+', '_', category.name).strip('_')
        if safe_name:
            filename = f'merch_items_{safe_name}.xlsx'

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
