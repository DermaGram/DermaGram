from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
from db.db import connection

def do_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    if POST_USERNAME == "":
        return login()
    # fetch password
    c, conn = connection()
    name = c.execute("SELECT username FROM DG_User WHERE username = (%s)", [thwart(POST_USERNAME)])
    pw = c.execute("SELECT password FROM DG_User WHERE username = (%s)", [thwart(POST_USERNAME)])
    pw = c.fetchone()[0]
    # encrypt entered password and check against queried password
    if sha256_crypt.verify(request.form['password'], pw):
        session['logged_in'] = True
        session['username'] = request.form['username']
    else:
        flash('wrong password!')
