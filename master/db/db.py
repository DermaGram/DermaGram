import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "dermagram",
                           passwd = "dermagram",
                           db = "Dermagram")
    c = conn.cursor()

    return c, conn

