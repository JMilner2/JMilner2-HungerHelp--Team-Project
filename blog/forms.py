"""
Author: Josh and Andrew
Description: This module defines a Flask form class named 'RecipeForm' used for capturing recipe details.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, FileField, FloatField
from wtforms.validators import DataRequired, NumberRange, Regexp, ValidationError
from flask_uploads import IMAGES, UploadSet, configure_uploads
from app import app
import re

# sets all the image file types to the variable images
images = UploadSet('images', IMAGES)
configure_uploads(app, images)


# validation for the price field using regex (1, 1.99, 1.00, not 1.9)
def validate_data(form, field):
    if not field.data:
        return
    pattern = re.compile(r"^\d+(\.\d{2})?$")
    if not pattern.match(field.data):
        raise ValidationError("Price must be in the proper format e.g. (1, 1.99, 10.00)")


# form class for uploading a recipe, all form fields must be filled in
class RecipeForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    recipe = StringField(validators=[DataRequired()])
    ingredients = StringField(validators=[DataRequired()])
    # only allows IMAGES to be uploaded
    image = FileField(validators=[
        FileAllowed(images, "only images are allowed"),
        FileRequired("file field should not be empty")
    ])
    price = StringField(validators=[DataRequired(), validate_data])
    submit = SubmitField()


# form class for editing a recipe, doesn't require all form fields to be filled
class EditRecipeForm(FlaskForm):
    title = StringField()
    recipe = StringField()
    ingredients = StringField()
    image = FileField(validators=[
        FileAllowed(images, "only images are allowed")])
    price = StringField(validators=[validate_data])
    submit = SubmitField()
