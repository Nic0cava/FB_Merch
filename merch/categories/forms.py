from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

from merch.models import Category

class AddCategoryForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    submit = SubmitField("Add New Category")

    def check_category_name(self,field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("This category name already exists!")
        
class UpdateCategoryForm(FlaskForm):

    name = StringField("Name",validators=[DataRequired()])
    submit = SubmitField("Update")

    def check_category_name(self,field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("This category name already exists!")