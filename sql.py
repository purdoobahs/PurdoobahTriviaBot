import sqlite3
import pandas

def initialize():
    conn, c = connectDB()
    c.execute("DROP TABLE players")
    c.execute("""CREATE TABLE players (
        name text,
        userID blob,
        gameScore integer,
        seasonScore integer,
        online integer
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

    c.execute("DROP TABLE specialAnswers")
    c.execute("""CREATE TABLE specialAnswers (
        name blob,
        round blob,
        numCorrect integer,
        points integer,
        answer1 blob,
        answer2 blob,
        answer3 blob,
        answer4 blob)
    """)
    conn.commit()
    conn.close()
    return

async def addPlayer(incominguser, ctx):
    conn, c = connectDB()
    c.execute("""SELECT name FROM players WHERE userID = ?""",(ctx.author.id,))
    list = c.fetchall()
    if(len(list) != 0):
        return -2, list[0]
    c.execute("""SELECT * FROM players WHERE name = ?""",(incominguser,))
    list = c.fetchall()
    if(len(list) != 0):
        return -1,list[0]
    c.execute("INSERT INTO players VALUES (?,?,?,?,?)", (incominguser, ctx.author.id,0, 0, 0))
    await ctx.send(f'Player {incominguser} added!')
    conn.commit()
    conn.close()

def findPlayer(userIDcheck):
    conn, c = connectDB()
    c.execute("""SELECT name FROM players WHERE userID = ?""",(userIDcheck,))
    list = c.fetchone()
    return list[0]

def findUserID(nameCheck):
    conn, c = connectDB()
    c.execute("""SELECT userID FROM players WHERE name = ?""",(nameCheck,))
    list = c.fetchone()
    return list[0]

def findPoints(points1, name1, round1, date1, question1):
    conn, c = connectDB()
    c.execute("""SELECT points, question FROM data WHERE (name = ? AND round = ? AND date = ?)""",(name1, round1, date1,))
    list = c.fetchall()
    for x in list:
        if x[0] == points1:
            if x[1] != int(question1):
                return 1
    conn.close()


def addAnswer(date1, round1, question1, name1, answer1, points1, correct1):
    conn, c = connectDB()
    c.execute("""SELECT * FROM data WHERE (name = ? AND round = ? AND question = ? AND date = ?)""",(name1, round1, question1, date1,))
    list = c.fetchone()
    if(list is not None):
        c.execute("""UPDATE data SET answer = ?, points = ?, correct = ? WHERE name = ? AND round = ? AND question = ? AND date = ?""", (answer1, points1, correct1, name1, round1, question1, date1,))
    else:
        c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?)", (date1, round1, question1, name1, answer1, points1, correct1,))
    conn.commit()
    conn.close()
    return

def addSpecial(name1, round1, numCorrect1, points1, args):
    conn, c = connectDB()
    c.execute("""SELECT * FROM specialAnswers WHERE name = ? AND round = ?""",(name1, round1,))
    list = c.fetchone()
    if(list is not None):
        c.execute("""UPDATE specialAnswers SET numCorrect=?, points=?, answer1=?, answer2=?, answer3=?,answer4=? WHERE name=? AND round=?""",(numCorrect1,points1,args[0],args[1],args[2],args[3],name1,round1,))
    else:
        c.execute("""INSERT INTO specialAnswers VALUES (?,?,?,?,?,?,?,?)""",(name1, round1, numCorrect1, points1, args[0],args[1],args[2],args[3],))
    conn.commit()
    conn.close()
    return

def getResponses(round1, question1, date1):
    conn, c = connectDB()
    c.execute("""SELECT name, answer, correct FROM data WHERE round=? AND question=? AND date=?""", (round1, question1, date1,))
    return c.fetchall()

def getSpecialResponses(round1):
    conn, c = connectDB()
    c.execute("""SELECT name, numCorrect, answer1, answer2, answer3, answer4, points FROM specialAnswers WHERE round=?""",(round1,))
    return c.fetchall()

def getResponse(round1, question1, date1, userData):
    conn, c = connectDB()
    name1 = findPlayer(userData.author.id)
    c.execute("""SELECT name, answer, correct FROM data WHERE round=? AND question=? AND date=? AND name=? """, (round1, question1, date1,name1,))
    return c.fetchone()

def getSpecialResponse(round1, userData):
    conn, c = connectDB()
    name1 = findPlayer(userData.author.id)
    c.execute("""SELECT name, numCorrect, points, answer1, answer2, answer3, answer4 FROM specialAnswers WHERE name=? AND round=?""", (name1, round1))
    return c.fetchone()

def connectDB():
    conn = sqlite3.connect('trivia.db')
    c = conn.cursor()
    return conn,c