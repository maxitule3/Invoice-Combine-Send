import sqlite3


#Path of SQL database
DATABASE_PATH = 'data.sqlite3'


def connect():
        return sqlite3.connect(DATABASE_PATH)