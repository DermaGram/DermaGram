from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from db.tabledef import *
from db.registrationClass import *
from db.db import connection
engine = create_engine('sqlite:///tutorial.db', echo=True)

from utils.imgur_utils import ImgurUtils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'

#TODO: remove this default values when db is available
album_id = 'cHPkw' #Album Name: ImgurPythonTest
imgur = ImgurUtils('ahearst',album_id)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('upload.html')

@app.route('/list_image_history')
def list_image_history():
    image_history = imgur.get_image_history()
    return render_template('list_image_history.html',image_history=image_history)

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    if POST_USERNAME == "":
        return login()

    c, conn = connection()
    name = c.execute("SELECT username FROM DG_User WHERE username = (%s)", [thwart(POST_USERNAME)])
    pw = c.execute("SELECT password FROM DG_User WHERE username = (%s)", [thwart(POST_USERNAME)])
    pw = c.fetchone()[0]

    if sha256_crypt.verify(request.form['password'], pw):
        session['logged_in'] = True
        session['username'] = request.form['username']
    else:
        flash('wrong password!')
    return login()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/register', methods=["GET","POST"])
def register():
    try:
        form = RegistrationForm(request.form)
        session['logged_in'] = False
        if request.method == "POST" and form.validate():
            username_p  = str(form.username.data)
            email = str(form.email.data)
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()
            x = c.execute("SELECT * FROM DG_User WHERE username = (%s)", [thwart(username_p)])
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO DG_User (username, password, email) VALUES (%s, %s, %s)", (username_p, password, email))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username_p

                return redirect(url_for('home'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
