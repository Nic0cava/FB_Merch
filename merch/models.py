# merch/models.py
from merch import db
from sqlalchemy import CheckConstraint, func
# from datetime import datetime, timezone


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
   # adds a non-negative constraint to quantity column
   __tablename__= 'items'
   __table_args__ = (
        CheckConstraint('quantity >= 0', name='ck_items_quantity_nonnegative'),
    )
   
   category = db.relationship(Category)

   id = db.Column(db.Integer, primary_key=True)
   category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

   name = db.Column(db.String(64),unique=True,nullable=False)
   quantity = db.Column(db.Integer, nullable=False, default=0)
   # date = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)) #! If this does not work try server-side
   # Server-Side #!might have to change pgAdmin settings
   date = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
   # relationship back to Category
   category = db.relationship('Category', back_populates='items')


   def __init__(self, name, quantity=0, category_id=None):
       self.name = name
       self.quantity = quantity
       self.category_id = category_id

   def __repr__(self):
       return f"Item: {self.name}, QT: {self.quantity}"

