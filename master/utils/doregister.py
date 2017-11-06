from flask import request
from db.registrationClass import *
from db.db import *

from utils.imgur_utils import ImgurUtils
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
                #TODO: this should be cleaned up
                imgur = ImgurUtils()
                album_id = imgur.create_new_album(user_info['username'])
                user_info['album_id'] = album_id
                cls._commit_user_info_to_db(c, conn, user_info)
                #TODO there is no album_id yet so get rid of 'blah' from initialziation of ImgurUtils
                SessionUtils.update_session_info(success, user_info['username'], user_info['username'], user_info['album_id'])

        return success

    @staticmethod
    def _get_registration_info(form):
        user_info = {}
        user_info["username"] = str(form.username.data)
        user_info["password"] = sha256_crypt.encrypt((str(form.password.data)))
        user_info["email"] = str(form.email.data)
        user_info['album_id'] = ""
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
        cursor.execute("INSERT INTO DG_User (username, password, email, albumLink) VALUES (%s, %s, %s, %s)",
                        (user_info['username'], user_info['password'], user_info['email'], user_info['album_id']) )
        connection.commit()
        cursor.close()
        connection.close()
        gc.collect()