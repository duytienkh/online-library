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
            'CREATE TABLE IF NOT EXISTS book ('
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
            'ext          TEXT,'
            'FOREIGN KEY (id) REFERENCES book(book_id)'
            ')'
        )


DATABASE_CONNECTION = Database('database/books.db')


def check_user_exists(username) -> bool:
    query = (
        'SELECT password '
        'FROM account '
        'WHERE username = ?'
    )
    return DATABASE_CONNECTION.conn.execute(query, (username, )).fetchone() is not None


def check_user_password(username, password) -> bool:
    query = (
        'SELECT 1 '
        'FROM account '
        'WHERE username = ? AND password = ?'
    )
    return DATABASE_CONNECTION.conn.execute(query, (username, password)).fetchone() is not None


def create_account(username, password) -> bool:
    query = (
        'INSERT INTO account (username, password)'
        'VALUES (?, ?)'
    )
    try:
        DATABASE_CONNECTION.conn.execute(query, (username, password))
    except Exception as e:
        print(e)
        return False
    return True
