# items/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

# Add Item Form
class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    # Ensures quantity can't be negative
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField("Category",coerce=int,)
    submit = SubmitField('Submit')

# Update Item Form
class UpdateItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Update Item")

# Delete Item Form
class DeleteItemForm(FlaskForm):
    submit = SubmitField("Delete")