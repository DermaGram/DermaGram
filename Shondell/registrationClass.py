### added for signin page 
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc


class RegistrationForm(Form):
    username = TextField('Enter a username', [validators.Length(min=6, max=50)])
    email = TextField('Enter your email', [validators.Length(min=6, max=50)])
    password = PasswordField('Enter a password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Your passwords must match')
    ])
    confirm = PasswordField('Confirm your password')
