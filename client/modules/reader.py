import base64
import tkinter as tk

import modules.commute as commute


def get_book_content(id):
    req = {
        "type": "book_content",
        "id": id,
        "log": "get book content"
    }

    return commute.send_n_recv(req)


def read(id):
    book = get_book_content(id)
    if book is None:
        return
    gui = tk.Tk()
    gui.title("Book reader")
    content = tk.Text(gui)
    if book["status"] is False:
        content.insert(tk.INSERT, book["log"])
    elif book["ext"] != "txt":
        content.insert(tk.INSERT, f'Cannot read book with {book["ext"]} extension.')
    else:
        content.insert(tk.INSERT, base64.b64decode(book["data"]).decode())
    content.pack()
    gui.mainloop()


def donwload(id):
    book_content = get_book_content(id)

    return book_content
