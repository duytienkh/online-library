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
            'author         TEXT,'
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


def look_up_books(book_id=None, book_name=None, book_type=None, author=None):
    """
        Get a list of books that match the given params
        Return a list of tuple (book_id, book_name, book_type, author, year)
    """
    query = (
        'SELECT * '
        'FROM book '
        'WHERE 1'
    )
    args = []
    if book_id is not None:
        query += ' AND book_id=?'
        args.append(book_id)
    if book_name is not None:
        query += ' AND book_name=?'
        args.append(book_name)
    if book_type is not None:
        query += ' AND book_type=?'
        args.append(book_type)
    if author is not None:
        query += ' AND author=?'
        args.append(author)

    return DATABASE_CONNECTION.conn.execute(query, args).fetchall()


def get_book_content(book_id):
    """
        Get content of a book
        Return a tuple (data, ext) with `data` is the
        binary data of the book. `ext` is extention
        of the file.
        Return None if book_id doesn't exist
    """
    query = (
        'SELECT content, ext '
        'FROM book_content '
        'WHERE bookid=?'
    )
    return DATABASE_CONNECTION.conn.execute(query, (book_id, )).fetchone()
