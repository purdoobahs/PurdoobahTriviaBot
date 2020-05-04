import sqlite3
import pandas

def initialize():
    conn, c = connectDB()
    c.execute("DROP TABLE players")
    c.execute("""CREATE TABLE players (
        name text,
        userID integer,
        seasonScore integer
        )""")

    c.execute("DROP TABLE data")
    c.execute("""CREATE TABLE data (
        date blob,
        round blob,
        question integer,
        name text,
        answer text,
        points integer,
        correct integer)
    """)
    conn.commit()
    conn.close()
    return

async def addPlayer(incominguser, ctx):
    conn, c = connectDB()
    score = 0
    c.execute("""SELECT name FROM players WHERE userID = ?""",(ctx.author.id,))
    list = c.fetchall()
    if(len(list) != 0):
        return -2, list[0]
    c.execute("""SELECT * FROM players WHERE name = ?""",(incominguser,))
    list = c.fetchall()
    if(len(list) != 0):
        return -1,list[0]
    c.execute("INSERT INTO players VALUES (?,?,?)", (incominguser, ctx.author.id,score))
    await ctx.send(f'Player {incominguser} added!')
    conn.commit()
    conn.close()

def findPlayer(userIDcheck):
    conn, c = connectDB()
    c.execute("""SELECT name FROM players WHERE userID = ?""",(userIDcheck,))
    list = c.fetchone()
    return list[0]

def addAnswer(date1, round1, question1, name1, answer1, points1, correct1):
    conn, c = connectDB()
    c.execute("""SELECT * FROM data WHERE (name = ? AND round = ? AND question = ? AND date = ?)""",(name1, round1, question1, date1,))
    list = c.fetchone()
    if(list is not None):
        c.execute("""UPDATE data SET answer = ?, points = ?, correct = ?""", (answer1, points1, correct1,))
        print('Updated value')
    else:
        print('Inserting value')
        c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?)", (date1, round1, question1, name1, answer1, points1, correct1,))
    conn.commit()
    conn.close()
    return

def connectDB():
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()
    return conn,c