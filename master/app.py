from flask import Flask, render_template, request, session
import os
from db.registrationClass import *

from utils.dologin import Login
from utils.doregister import SignUp
from utils.doUpload import Upload
from utils.db_utils import DbUtils
from utils.imgur_utils import ImgurUtils

# Initialize App w/ config
app = Flask(__name__)
# TODO: move all config related stuff to separate app config class
Upload = Upload()
Upload.initialize_app_upload(app)


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
    imgur = ImgurUtils()

    if request.method == 'POST' and request.files:
        image_name = Upload.upload_image(session['album_id'], request.files['photo'])
        if not image_name:
            print "ERROR failed to upload image: ", image_name

    #get latest image from album, if there is one
    image = {
        'id': "3sacjQ6",
        'title': "Surfs Up!"
    }
    # TODO: get album id from the db!
    album_id = 'cHPkw'
    image_table = imgur.get_image_history( album_id )
    image_carousel = ['https://imgur.com/Zyv8Daj.jpg','https://imgur.com/1cXDeXR.jpg','https://imgur.com/zrxq7h9.jpg','https://imgur.com/WfbtvAb.jpg']
    return render_template("profile.html", image=image, image_carousel=image_carousel, image_table=image_table)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
