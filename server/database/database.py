import sqlite3


class Database():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        self.conn.execute(
            'CREATE TABLE IF NOT EXISTS account ('
            'username   TEXT PRIMARY KEY,'
            'password   TEXT'
            ')'
        )

        self.conn.execute(
            'CREATE TABLE IF NOT EXISTS book_info ('
            'book_id        INTEGER PRIMARY KEY,'
            'book_name      TEXT,'
            'book_type      TEXT,'
            'author_name    TEXT,'
            'year           INTEGER'
            ')'
        )

        self.conn.execute(
            'CREATE TABLE IF NOT EXISTS book_content ('
            'id           INTEGER PRIMARY KEY,'
            'content      BLOB,'  # binary datatype
            'ext          TEXT'
            ')'
        )


DATABASE_CONNECTION = Database('database/books.db')
