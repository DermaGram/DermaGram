from db import connection 

def getAlbum():
    username = session['username']
    c, conn = connection()
    album = c.execute("SELECT albumLink FROM DG_User WHERE username = (%s)", [thwart(username)])
    album = c.fetchone()[0]
    return album
