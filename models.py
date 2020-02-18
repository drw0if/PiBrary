import sqlite3
from datetime import datetime as dt

"""
Book:
    id (incremental)
    name
    extension
    hash (stored name)
    uploader_ip
    uploader_username (optional)
    upload_time

Vote:
    book_id
    value
    comment (optional)
    username (optional)

"""

DBNAME = 'library.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

        # create tables if not exists
        self.createBookTable()
        self.createVoteTable()

    def createBookTable(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Book"(
            id INTEGER PRIMARY KEY,
            name TEXT,
            extension VARCHAR(10),
            hash CHAR(64),
            uploader_ip VARCHAR(15),
            uploader_username TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(query)

    def createVoteTable(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Vote"(
            id INTEGER PRIMARY KEY,
            value INTEGER,
            comment TEXT,
            username TEXT,

            book_id INTEGER FOREIGNKEY REFERENCES Book(id)
        );
        """
        self.conn.execute(query)


class Book:
    def __init__(self):
        self.TABLENAME = 'Book'
        self.conn = sqlite3.connect(DBNAME)
        self.conn.row_factory = dict_factory

    def create(self, name, extension, uploader_ip, uploader_username=None):
        _hash = str(hash(name))
        query = f"""
        INSERT INTO "{self.TABLENAME}"(name, extension, hash, uploader_ip, uploader_username)
        VALUES (?, ?, ?, ?, ?);
        """
        values = (name, extension, _hash, uploader_ip, uploader_username)

        c = self.conn.cursor()
        c.execute(query, values)
        self.conn.commit()

    def select(self):
        query = f"""
        SELECT * FROM {self.TABLENAME};
        """
        c = self.conn.cursor()
        c.execute(query)
        return c.fetchall()


class Vote:
    def __init__(self):
        self.TABLENAME = 'Vote'
        self.conn = sqlite3.connect(DBNAME)
        self.conn.row_factory = dict_factory

    def create(self, book_id, value, comment=None, username=None):
        query = f"""
        INSERT INTO "{self.TABLENAME}"(value, comment, username, book_id)
        VALUES (?, ?, ?, ?);
        """
        values = (value, comment, username, book_id)

        c = self.conn.cursor()
        c.execute(query, values)
        self.conn.commit()

    def select(self, book_id):
        query = f"""
        SELECT * FROM {self.TABLENAME} WHERE book_id = ?;
        """
        values = book_id,
        c = self.conn.cursor()
        c.execute(query, values)
        return c.fetchall()
