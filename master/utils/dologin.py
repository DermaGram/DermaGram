from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
from db.db import connection

def do_login():
    username = str(request.form['username'])
    password = str(request.form['password'])
    if username == "":
        session['logged_in'] = False
	return
    # fetch password
    c, conn = connection()
    name = c.execute("SELECT username FROM DG_User WHERE username = (%s)", [thwart(username)])
    if int(name) == 0:
	session['logged_in'] = False
	return
    pw = c.execute("SELECT password FROM DG_User WHERE username = (%s)", [thwart(password)])
    pw = c.fetchone()[0]
    # encrypt entered password and check against queried password
    if sha256_crypt.verify(password, pw):
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('wrong password!')
