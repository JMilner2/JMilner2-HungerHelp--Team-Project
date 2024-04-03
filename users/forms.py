"""
Author: Shaikha Almajed
Description: This code defines Flask forms for user registration and login
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length
import re
from flask_wtf import RecaptchaField


# A function that excludes some special characters
def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")


# A regex function that specifies that digits must be in the form: XXXX-XXX-XXXX
def validate_phone(form, phone):
    p = re.compile(r"\d{4}[-]\d{3}[-]\d{4}$")
    if not p.match(phone.data):
        raise ValidationError("Invalid phone number, must be in the form XXXX-XXX-XXXX")


# A regex function that specifies that it must contain at least 1 digit and at least
# 1 lowercase word character and at least 1 uppercase word character and at least 1 special character
def validate_pass(form, password):
    p = re.compile(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W+)")
    if not p.match(password.data):
        raise ValidationError("Must contain at least 1 digit, 1 lowercase word character, "
                              "1 uppercase word character and 1 special character ")


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(),
                                    Email()])
    firstname = StringField(validators=[DataRequired(),
                                        character_check])
    lastname = StringField(validators=[DataRequired(),
                                       character_check])
    phone = StringField(validators=[DataRequired(),
                                    validate_phone])
    password = PasswordField(validators=[DataRequired(),
                                         Length(min=6, max=12),
                                         validate_pass])
    confirm_password = PasswordField(validators=[DataRequired(),
                                                 EqualTo('password', message='Both password fields must be equal!')])
    notifications = BooleanField(label='Receive notifications')

    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()
