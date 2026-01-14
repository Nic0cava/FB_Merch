# merch/models.py
from merch import db
from sqlalchemy import CheckConstraint, func
from sqlalchemy.ext.hybrid import hybrid_property
# from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash


class Category(db.Model):
   
    __tablename__ = 'categories'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,nullable=False)

    # relationship to Item (class name must match)
    items = db.relationship(
        'Item',
        back_populates='category',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Category Name: {self.name}"

class Item(db.Model):
   __tablename__= 'items'
   __table_args__ = (
        CheckConstraint('foh_qty >= 0', name='ck_items_foh_qty_nonnegative'),
        CheckConstraint('boh_qty >= 0', name='ck_items_boh_qty_nonnegative'),
        CheckConstraint('room_300_qty >= 0', name='ck_items_room_300_qty_nonnegative'),
        CheckConstraint('item_cost >= 0', name='ck_items_item_cost_nonnegative'),
        CheckConstraint('prior_month_total >= 0', name='ck_items_prior_month_total_nonnegative'),
    )
   
   category = db.relationship(Category)
   monthly_total = db.relationship(
       'ItemMonthlyTotal',
       back_populates='item',
       uselist=False,
       cascade='all, delete-orphan'
   )

   id = db.Column(db.Integer, primary_key=True)
   category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

   name = db.Column(db.String(64),unique=True,nullable=False)

   # New quantity columns
   foh_qty = db.Column(db.Integer, nullable=False, default=0)
   boh_qty = db.Column(db.Integer, nullable=False, default=0)
   room_300_qty = db.Column(db.Integer, nullable=False, default=0)

   # Monthly tracking (stored for export)
   prior_month_total = db.Column(db.Integer, nullable=False, default=0)
   difference = db.Column(db.Integer, nullable=False, default=0)
   
   # Item cost as float
   item_cost = db.Column(db.Float, nullable=False, default=0.0)

   
   # date = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)) #! If this does not work try server-side
   # Server-Side #!might have to change pgAdmin settings
   date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
   # relationship back to Category
   category = db.relationship('Category', back_populates='items')

   # Calculated properties
   @hybrid_property
   def total_qty(self):
       """Sum of all quantity fields"""
       return (self.foh_qty or 0) + (self.boh_qty or 0) + (self.room_300_qty or 0)

   @hybrid_property
   def total_cost(self):
       """Total quantity multiplied by item cost"""
       return self.total_qty * (self.item_cost or 0.0)



   def __init__(
       self,
       name,
       foh_qty=0,
       boh_qty=0,
       room_300_qty=0,
       item_cost=0.0,
       category_id=None,
       prior_month_total=0,
       difference=0,
   ):
       self.name = name
       self.foh_qty = foh_qty
       self.boh_qty = boh_qty
       self.room_300_qty = room_300_qty
       self.item_cost = item_cost
       self.category_id = category_id
       self.prior_month_total = prior_month_total
       self.difference = difference

   def __repr__(self):
       return f"Item: {self.name}, Total QT: {self.total_qty}"


class ItemMonthlyTotal(db.Model):
   __tablename__ = 'item_monthly_totals'

   id = db.Column(db.Integer, primary_key=True)
   item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False, unique=True)
   month_end = db.Column(db.DateTime(timezone=True), nullable=False)
   total_qty = db.Column(db.Integer, nullable=False, default=0)

   item = db.relationship('Item', back_populates='monthly_total')


# A single shared password to gate the whole app
class AppAuth(db.Model):
   __tablename__ = 'app_auth'

   id = db.Column(db.Integer, primary_key=True)
   password_hash = db.Column(db.String(255), nullable=False)
   updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

   @staticmethod
   def set_password(plaintext: str):
       rec = AppAuth.query.get(1)
       if rec is None:
           rec = AppAuth(id=1, password_hash=generate_password_hash(plaintext))
           db.session.add(rec)
       else:
           rec.password_hash = generate_password_hash(plaintext)
       db.session.commit()

   @staticmethod
   def verify_password(plaintext: str) -> bool:
       rec = AppAuth.query.get(1)
       if not rec or not rec.password_hash:
           return False
       return check_password_hash(rec.password_hash, plaintext)
