from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from registrationClass import * 
engine = create_engine('sqlite:///tutorial.db', echo=True)
from db import connection
 
app = Flask(__name__)
 
@app.route('/')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return home(); 

@app.route('/home')
def home():
    return render_template('home2.html')

@app.route('/about')
def about():
    return render_template('about2.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return login()
 
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return login()

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
            x = c.execute("SELECT * FROM DG_User WHERE username = (%s)", 
                          [thwart(username_p)])
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
