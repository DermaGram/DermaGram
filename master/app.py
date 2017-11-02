from flask import Flask, render_template, request, session
import os
from db.registrationClass import *

from utils.dologin import Login
from utils.doregister import SignUp
from utils.imgur_utils import ImgurUtils

app = Flask(__name__)
#TODO: is this secret key needed?
app.config['SECRET_KEY'] = 'DontTellAnyone'

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

@app.route('/profile')
def display_profile():
    #get latest image from album, if there is one
    image = {
        'id': "3sacjQ6",
        'title': "Surfs Up!"
    }
    image_history = imgur.get_image_history()
    return render_template("profile.html", image=image, image_history=image_history)

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


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
