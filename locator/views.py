"""
Author: Vilius
Description: This module defines a Flask blueprint for a location-based feature.
"""
from flask import Blueprint, render_template
from locator.forms import LocatorForm

# Create a blueprint for the locator module
locator_blueprint = Blueprint('locator', __name__, template_folder='templates')


@locator_blueprint.route('/locator', methods=['Get', 'POST'])
def locator():
    form = LocatorForm()
    # Check if all form validators pass
    if form.validate_on_submit():
        # Replace spaces in the location string with "%20" for URL compatibility
        string = form.location.data.replace(" ", "%20")
        # Construct the URL for embedding Google Maps
        url = "https://www.google.com/maps/embed/v1/search?q=Food%20Banks%20near%20" + string +\
              "&key=AIzaSyD1yWxUGKH3gn5gHUaG92l3vlReStdixys"
        # Render the locator template with the form, URL, and a flag indicating successful form submission
        return render_template('locator/locator.html', form=form, url=url, render=1)
    # Render the locator template with the form and a flag indicating unsuccessful form submission
    return render_template('locator/locator.html', form=form, render=0)


