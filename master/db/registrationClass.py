# Used with register.html, creates a form class to be used to pull data from the browser
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.validators import Email
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart # used in function register() in app.py
import gc
# define input fields and sets errors for bad input
class RegistrationForm(Form):
    username = TextField('Enter a username', [validators.Length(min=6, max=50)])
    email = TextField('Enter your email', [validators.Length(min=6, max=50),validators.Email("Not a valid email address")])
    password = PasswordField('Enter a password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Your passwords must match')
    ])
    confirm = PasswordField('Confirm your password')
