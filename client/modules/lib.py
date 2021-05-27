import tkinter as tk
from tkinter import ttk

import modules.commute as commute
import modules.reader as reader


def lib_gui():
    gui = tk.Tk()
    gui.title("Online Library")
    # finding frame
    f_frame = tk.Frame(gui)
    f_content = tk.Entry(f_frame)
    f_content.pack(side=tk.LEFT)
    options = tk.StringVar(f_frame)
    options.set("ID")
    f_options = tk.OptionMenu(f_frame, options, "ID", "Name", "Type", "Author", "Year")
    f_options.pack(side=tk.LEFT)
    f_btn = tk.Button(f_frame, text="Find")
    f_btn.pack(side=tk.LEFT)
    f_frame.pack()
    # result frame
    book_list = ttk.Treeview(gui, columns=(1, 2, 3, 4, 5), show="headings")
    config_colum = [('ID', 10), ('Name', 250), ('Type', 90), ('Author', 110), ('Year', 50)]
    for num, col in enumerate(config_colum):
        name, width = col
        book_list.heading(num + 1, text=name)
        book_list.column(num + 1, width=width)
    book_list.pack()
    # book info
    info_frame = tk.Frame(gui)
    info_frame.pack()

    def item_selected(event):
        for selected_item in book_list.selection():
            item = book_list.item(selected_item)
            record = item['values']
            show_book_info(info_frame, record)

    book_list.bind('<<TreeviewSelect>>', item_selected)

    f_btn.config(command=lambda: find(book_list, f_content, options))

    gui.mainloop()


def find(book_list, content, option):
    req = {
        "type": "find",
        "content": content.get(),
        "option": option.get(),
        "log": "find book"
    }
    book_list.delete(*book_list.get_children())
    books = commute.send_n_recv(req)
    if books:
        for book_info in books["data"]:
            book_list.insert("", tk.END, values=book_info)


def show_book_info(f, record):
    for e in f.winfo_children():
        e.destroy()
    tk.Label(f, text=f"ID: {record[0]}").pack()
    tk.Label(f, text=f"Name: {record[1]}").pack()
    tk.Label(f, text=f"Type: {record[2]}").pack()
    tk.Label(f, text=f"Author: {record[3]}").pack()
    tk.Label(f, text=f"Year: {record[4]}").pack()
    btn_frame = tk.Frame(f)
    btn_frame.pack()
    read_btn = tk.Button(btn_frame, text="Read")
    dl_btn = tk.Button(btn_frame, text="Download")
    read_btn.pack(side=tk.LEFT, padx=10)
    dl_btn.pack(side=tk.LEFT, padx=10)
    read_btn.config(command=lambda: reader.read(record[0]))
    dl_btn.config(command=lambda: reader.donwload(record[0]))
