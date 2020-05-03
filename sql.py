import sqlite3
import pandas

conn = sqlite3.connect('trivia.db')

c = conn.cursor()

# c.execute("""CREATE TABLE players (
#     name text,
#     userID integer
#     )""")

# c.execute("DROP TABLE data")
#
# c.execute("""CREATE TABLE data (
#     date blob,
#     round blob,
#     question integer,
#     name text,
#     answer text,
#     points integer,
#     correct integer)
# """)


def addPlayer(incominguser, incominguserID):
    conn, c = connectDB()
    c.execute("""SELECT name FROM players WHERE userID = ?""",(incominguserID,))
    list = c.fetchall()
    if(len(list) != 0):
        return -2, list[0]
    c.execute("""SELECT * FROM players WHERE name = ?""",(incominguser,))
    list = c.fetchall()
    if(len(list) != 0):
        return -1,list[0]
    c.execute("INSERT INTO players VALUES (?,?)", (incominguser, incominguserID))
    conn.commit()
    conn.close()
    return

def connectDB():
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()
    return conn,c