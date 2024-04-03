"""
Author: Vilius
Description: This module defines a Flask form class called 'LocatorForm' used
 for capturing user input for location-based searches.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Define a form for the locator module
class LocatorForm(FlaskForm):
    location = StringField(validators=[DataRequired()])
    submit = SubmitField()
