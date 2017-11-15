from flask import request, session
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
from db.db import connection

from utils.db_utils import DbUtils
from utils.session_utils import SessionUtils
from utils.logging_utils import LoggingUtils
import logging
LoggingUtils.initialize_logger(__name__)

class Login:

    @classmethod
    def do_login(cls):
        logger = logging.getLogger(__name__)
        success = False
        c, conn = connection()

        # fetch and validate username
        username = str(request.form['username'])
        success = cls._is_username_valid(c, username)

        # fetch and validate password
        if success:
            password = str(request.form['password'])
            success = cls._is_password_valid(c, username, password)

        # fetch and validate album info
        # TODO - fetch album_name && album_id

        # update user session info
        #TODO: replace album_name && album_id with whatever we get from db
        album_id = DbUtils.get_album_id(username)
        #NOTE album_name is the same as the username
        SessionUtils.update_session_info(success, username, username, album_id)
        return success

    @staticmethod
    def _is_username_valid(cursor, username):
        logger = logging.getLogger(__name__)
        success = True

        if not username:
            logger.error("Username is empty sting.")
            flash("Enter a username")
            success = False
        else:
            name = cursor.execute("SELECT username FROM DG_User WHERE username = (%s)", [thwart(username)])
            if int(name) == 0:
                logger.error("Username {0} doesn't exist".format(username))
                flash("This username does not exist")
                success = False

        return success

    @staticmethod
    def _is_password_valid(cursor, username, password):
        logger = logging.getLogger(__name__)
        success = False

        pw = cursor.execute("SELECT password FROM DG_User WHERE username = (%s)", [thwart(username)])
        pw = cursor.fetchone()[0]

        # encrypt entered password and check against queried password
        if sha256_crypt.verify(password, pw):
            success = True
        else:
            logger.error("Password {0} is incorrect.".format(password))
            flash("Incorrect password")

        return success

