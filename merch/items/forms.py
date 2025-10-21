# items/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange
from wtforms import ValidationError

from merch.models import Item

# Add Item Form
class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    # Ensures quantity can't be negative
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField("Category",coerce=int,)
    submit = SubmitField('Submit')

    # WTForms validator must be named validate_<fieldname>
    def validate_name(self, field):
        if Item.query.filter_by(name=field.data).first():
            raise ValidationError("This item name already exists!")

# Update Item Form
class UpdateItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Update Item")

    def __init__(self, original_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, field):
        # allow same name as before, otherwise enforce uniqueness
        if field.data != self.original_name and Item.query.filter_by(name=field.data).first():
            raise ValidationError("This item name already exists!")

# Delete Item Form
class DeleteItemForm(FlaskForm):
    submit = SubmitField("Delete")