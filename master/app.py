from flask import Flask, render_template, request, session
import os
from db.registrationClass import *

from utils.dologin import Login
from utils.doregister import SignUp
from utils.doUpload import Upload
from utils.db_utils import DbUtils
from utils.tf_utils import TfUtils
from utils.imgur_utils import ImgurUtils
from utils.file_utils import FileUtils

#delete random lib after we add in classification
import random

# Initialize App w/ config
app = Flask(__name__)
# TODO: move all config related stuff to separate app config class
#Upload = Upload()
#Upload.initialize_app_upload(app)
fu = FileUtils()
photo_set = fu.get_upload_set()
fu.initialize_app_image_storage(app,photo_set)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_in'):
            #TODO need to update session info here if person goes directly to profile so we have album_id
            return profile()
    elif request.method == 'POST':
        if Login.do_login():
            #TODO when profile() called and profile.html rendered, it still shows localhost:5000/login, why?
            # session information is loaded from dologin.py
            return profile()

    return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm(request.form)
    # use form from register.html and pull data from that form
    if request.method == "POST" and form.validate():
        success = SignUp.do_register(form) # successful registration?
        if(success == False):
            return register() # reload sign up page
        else: 
            return login() # log them in
    return render_template("register.html", form=form)

#TODO add profile link so that after you login you can return without clicking on login (maybe use a person icon instead of 'login')
@app.route('/profile', methods=['GET','POST'])
def profile():
    image_link = ""
    classification_data = []

    if request.method == 'POST' and request.files:
        fu.refresh_temp_folder()
        photo_set.save(request.files['photo'])
        image_path = fu.get_image_file_path()
        classification_data = TfUtils.get_classifications(image_path)
        top_classification = TfUtils.get_top_classification(classification_data)
        image_link = Upload.upload_image(request.files['photo'].filename, image_path, request.form['inputLocation'], top_classification)
        fu.rm_files_temp_folder()
        if not image_link:
            print "ERROR failed to upload image: ", image_link

    imgur = ImgurUtils()
    images_data = imgur.get_images_from_album( session['album_id'] )
    return render_template("profile.html",
                           image_link=image_link,
                           image_table=images_data['table'],
                           classification_data=classification_data)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
