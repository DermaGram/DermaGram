from flask import Flask, render_template, request, session
import os
from db.registrationClass import *

from utils.dologin import Login
from utils.doregister import SignUp
from utils.imgur_utils import ImgurUtils

from upload.upload_function import Upload
from flask_uploads import UploadSet, IMAGES, configure_uploads
photos = UploadSet('photos', IMAGES)


app = Flask(__name__)
#TODO: is this secret key needed?
app.config['SECRET_KEY'] = 'DontTellAnyone'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

#TODO: we shouldn't initialize w/ album name/id since this will change with every user session
imgur = ImgurUtils('ImgurPythonTest','cHPkw')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_in'):
            return display_profile()
    elif request.method == 'POST':
        if Login.do_login():
            # session information is laoded from dologin.py
            return display_profile()

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
@app.route('/profile')
def display_profile():
    #get latest image from album, if there is one
    image = {
        'id': "3sacjQ6",
        'title': "Surfs Up!"
    }
    image_table = imgur.get_image_history()
    image_carousel = ['https://imgur.com/Zyv8Daj.jpg','https://imgur.com/1cXDeXR.jpg','https://imgur.com/zrxq7h9.jpg','https://imgur.com/WfbtvAb.jpg']
    return render_template("profile.html", image=image, image_carousel=image_carousel, image_table=image_table)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    run = Upload()
    run.upload_file()
    return render_template('confirm.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
