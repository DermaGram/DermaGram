from flask import request
from db.registrationClass import *
from db.db import *

from utils.session_utils import SessionUtils
from utils.logging_utils import LoggingUtils
import logging

LoggingUtils.initialize_logger(__name__)

class SignUp:

    @classmethod
    def do_register(cls, Form):
        logger = logging.getLogger(__name__)
        success = False

        # use form from register.html and pull data from that form
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            user_info = cls._get_registration_info(form)
            c, conn = connection()

            # fetch and validate username
            success = cls._is_username_valid(c, user_info['username'])
            if success:
                cls._commit_user_info_to_db(c, conn, user_info)
                # TODO: use ImgurUtils to create new album for this user
                # TODO: replace album_name && album_id with whatever we get from db

            SessionUtils.update_session_info(success, user_info['username'], 'ImgurPythonTest', 'cHPkw')
        return success

    @staticmethod
    def _get_registration_info(form):
        user_info = {}
        user_info["username"] = str(form.username.data)
        user_info["password"] = sha256_crypt.encrypt((str(form.password.data)))
        user_info["email"] = str(form.email.data)
        return user_info

    @staticmethod
    def _is_username_valid(cursor, username):
        logger = logging.getLogger(__name__)
        x = cursor.execute("SELECT username FROM DG_User WHERE username = (%s)", [thwart(username)])
        if int(x) > 0:  # if username exists
            logger.error("Username already exists.")
            return False
        return True

    @staticmethod
    def _commit_user_info_to_db(cursor, connection, user_info):
        cursor.execute("INSERT INTO DG_User (username, password, email) VALUES (%s, %s, %s)",
                        (user_info['username'], user_info['password'], user_info['email']) )
        connection.commit()
        cursor.close()
        connection.close()
        gc.collect()