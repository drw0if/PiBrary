import sqlite3
from datetime import datetime as dt

"""
Book:
    id (incremental)
    name
    uploader_ip
    uploader_username (optional)
    upload_time

Vote:
    book_id
    value
    review (optional)
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
            uploader_ip VARCHAR(15),
            uploader_username VARCHAR(20),
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(query)

    def createVoteTable(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Vote"(
            id INTEGER PRIMARY KEY,
            value INTEGER CHECK(value BETWEEN 1 AND 5),
            review TEXT,
            username VARCHAR(20),

            book_id INTEGER FOREIGNKEY REFERENCES Book(id)
        );
        """
        self.conn.execute(query)


class Book:
    def __init__(self):
        self.TABLENAME = 'Book'
        self.conn = sqlite3.connect(DBNAME)
        self.conn.row_factory = dict_factory

    def create(self, name, uploader_ip, uploader_username=None):
        query = f"""
        INSERT INTO "{self.TABLENAME}"(name, uploader_ip, uploader_username)
        VALUES (?, ?, ?);
        """
        values = (name, uploader_ip, uploader_username)

        c = self.conn.cursor()
        c.execute(query, values)
        self.conn.commit()

    def all(self):
        query = f"""
        SELECT * FROM "{self.TABLENAME}";
        """
        c = self.conn.cursor()
        c.execute(query)
        return c.fetchall()

    def select(self, _id):
        query = f"""
        SELECT *
        FROM "{self.TABLENAME}"
        WHERE id = ?;
        """
        values = _id,

        c = self.conn.cursor()
        c.execute(query, values)
        return c.fetchone()


class Vote:
    def __init__(self):
        self.TABLENAME = 'Vote'
        self.conn = sqlite3.connect(DBNAME)
        self.conn.row_factory = dict_factory

    def create(self, book_id, value, review=None, username=None):
        query = f"""
        INSERT INTO "{self.TABLENAME}"(value, review, username, book_id)
        VALUES (?, ?, ?, ?);
        """
        values = (value, review, username, book_id)

        c = self.conn.cursor()
        try:
            c.execute(query, values)
        except sqlite3.IntegrityError:
            raise ValueError
        self.conn.commit()

    def pickRandom(self, book_id):
        query = f"""
        SELECT * 
        FROM {self.TABLENAME}
        WHERE book_id = ? AND review IS NOT NULL
        ORDER BY RANDOM()
        LIMIT 5;
        """
        values = book_id,
        
        c = self.conn.cursor()
        c.execute(query, values)
        return c.fetchall()

    def avg(self, _id):
        query = f"""
        SELECT avg(value) as vote 
        FROM {self.TABLENAME} 
        WHERE book_id = ?;
        """
        values = _id,

        c = self.conn.cursor()
        c.execute(query, values)
        return c.fetchone()
