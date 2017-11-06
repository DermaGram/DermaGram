
from db.registrationClass import *
from db.db import *

#TODO make more functions that are used across different applications
#TODO add logging

class DbUtils:

    #TODO close connection and other proper db stuff
    @staticmethod
    def get_album_id(username):
        album_id = ""
        c, conn = connection()
        x = c.execute("SELECT albumLink FROM DG_User WHERE username = (%s)", [thwart(username)])
        if x:
            data = c.fetchall()
            for row in data:
                album_id = row[0]
                break
        return album_id
