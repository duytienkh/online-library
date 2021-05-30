import base64
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import modules.commute as commute


def get_book_content(id):
    req = {
        "type": "book_content",
        "id": id,
        "log": "Get book's content"
    }

    return commute.send_n_recv(req)


def read(id):
    book = get_book_content(id)
    if book is None:
        return
    gui = tk.Tk()
    gui.title("Book reader")
    scrollbar = tk.Scrollbar(gui)
    scrollbar.pack(side=tk.RIGHT, fill='y')
    content = tk.Text(gui, yscrollcommand=scrollbar.set)
    if book["status"] is False:
        content.insert(tk.INSERT, book["log"])
    elif book["ext"] != "txt":
        content.insert(tk.INSERT, f'Cannot read book with {book["ext"]} extension.')
    else:
        content.insert(tk.INSERT, base64.b64decode(book["data"]).decode())
    content.pack(padx=10, pady=10)
    gui.mainloop()


def donwload(id):
    book = get_book_content(id)
    if book is None:
        return
    if book["status"] is False:
        messagebox.showerror("Error", f"Error while downloading book id={id}: {book['log']}")
        return
    ext = book["ext"]
    fileName = filedialog.asksaveasfilename(defaultextension="." + ext, filetypes=((ext, "." + ext),))
    if fileName:
        try:
            open(fileName, 'wb').write(base64.b64decode(book["data"]))
            messagebox.showinfo("Downloaded", f"Downloaded successfully to `{fileName}`")
        except Exception as e:
            messagebox.showerror("Error", f"Error while saving to `{fileName}`: {e}")
