from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

from merch.models import Category

class AddCategoryForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    submit = SubmitField("Add New Category")

    # WTForms validator must be named validate_<fieldname>
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("This category name already exists!")
        
class UpdateCategoryForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    submit = SubmitField("Update")

    def __init__(self, original_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, field):
        # allow same name as before, otherwise enforce uniqueness
        if field.data != self.original_name and Category.query.filter_by(name=field.data).first():
            raise ValidationError("This category name already exists!")

class DeleteCategoryForm(FlaskForm):
    submit = SubmitField("Delete")