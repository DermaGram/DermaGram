from flask import session

class SessionUtils:

    @staticmethod
    def update_session_info(logged_in, username, album_name, album_id):
        '''@param logged_in: boolean
        @param username: string
        @param album_name: string
        @param album_id: string'''
        session['logged_in'] = logged_in
        session['username'] = username
        session['album_name'] = album_name
        session['album_id'] = album_id