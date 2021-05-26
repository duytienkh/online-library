import tkinter as tk

import modules.commute as commute


def get_book_content(id):
    req = {
        "type": "book_content",
        "id": id,
        "log": "get book content"
    }

    commute.send(req)
    res = commute.recv()

    return res


def read(id):
    gui = tk.Tk()
    gui.title("Book reader")
    book_content = get_book_content(id)
    content = tk.Text()
    content.insert(tk.INSERT, book_content)
    content.pack()
    gui.mainloop()


def donwload(id):
    book_content = get_book_content(id)

    return book_content
