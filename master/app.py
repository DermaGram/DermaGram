from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from db.registrationClass import *
from db.db import connection
from utils.dologin import do_login
from utils.doregister import *

from utils.imgur_utils import ImgurUtils
from upload.upload_function import SClass
from flask_uploads import UploadSet, IMAGES, configure_uploads
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'

#TODO: remove these default values when db is available
#       and we can dynamically populate user_data
user_data = {
    'uuid': 'ahearst1',
    'album_name': 'ImgurPythonTest',
    'album_id': 'cHPkw'
}
imgur = ImgurUtils(user_data['uuid'],user_data['album_id'])

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('upload.html')

@app.route('/profile')
def display_profile():
    image = {
        'id': "3sacjQ6",
        'title': "Surfs Up!"
    }
    image_history = imgur.get_image_history()
    return render_template("profile.html", image=image, image_history=image_history)

@app.route('/login', methods=['POST'])
def do_admin_login():
    do_login()
    return login()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm(request.form)
    # use form from register.html and pull data from that form
    if request.method == "POST" and form.validate():
        success = do_register(form) # successful registration? 
        if(success == False):
            return register() # reload sign up page
        else: 
            return login() # log them in
    return render_template("register.html", form=form)


'''
The following functions should be used to test the individual components
that make up the main Profile page.
Note: We should do this for all of our components
'''
# This should be rendered within the user's main profile page
@app.route('/list_image_history')
def list_image_history():
    image_history = imgur.get_image_history()
    return render_template('list_image_history.html',image_history=image_history)

# This should be rendered within the user's main profile page
@app.route('/display_image')
def display_image():
    image = {
        'id': "3sacjQ6",
        'title': "Surfs Up!"
    }
    return render_template('display_image.html',image=image)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    run = SClass()
    run.upload_file()
    return render_template('confirm.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
