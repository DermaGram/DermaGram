from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from db.registrationClass import *
from db.db import *

def do_register(Form): 
    status = False
    form = RegistrationForm(request.form)
    # use form from register.html and pull data from that form
    if request.method == "POST" and form.validate():
        username_p  = str(form.username.data)
        email = str(form.email.data)
        password = sha256_crypt.encrypt((str(form.password.data)))
        # query username 
        c, conn = connection()
        x = c.execute("SELECT username FROM DG_User WHERE username = (%s)", [thwart(username_p)])
        if int(x)>0: # if username exists 
            flash("That username is already taken, please choose another")
            status = False
            return status

        else: # insert data into database 
            c.execute("INSERT INTO DG_User (username, password, email) VALUES (%s, %s, %s)", (username_p, password, email))
            conn.commit()
            flash("Thanks for registering!")
            c.close()
            conn.close()
            gc.collect()
            session['logged_in'] = True
            session['username'] = username_p
            status = True
            return status
    return status
