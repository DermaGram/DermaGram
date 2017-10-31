from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
from db.db import connection
from utils.logging_utils import LoggingUtils

LoggingUtils.initialize_logger(__name__)

def do_login():
    logger = logging.getLogger(__name__)
    username = str(request.form['username'])
    password = str(request.form['password'])
    logger.info( "Attempting login for {0}".format(username))
    if username == "":
        session['logged_in'] = False
	logger.error("No username specified")
	return
    # fetch password
    c, conn = connection()
    name = c.execute("SELECT username FROM DG_User WHERE username = (%s)", [thwart(username)])
    if int(name) == 0:
	session['logged_in'] = False
	logger.error("Username {0} doesn't exist".format(username))
	return
    pw = c.execute("SELECT password FROM DG_User WHERE username = (%s)", [thwart(password)])
    pw = c.fetchone()[0]
    # encrypt entered password and check against queried password
    if sha256_crypt.verify(password, pw):
        session['logged_in'] = True
        session['username'] = username
	logger.info("User {0} is logged in".format(username))
    else:
	logger.error("Incorrect password")
