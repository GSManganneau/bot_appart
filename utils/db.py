import sqlite3
db = "rentBot.db"


def update(query):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()


def retrieve(query):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
