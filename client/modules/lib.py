import tkinter as tk
from tkinter import Text, ttk

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
    f_options = tk.OptionMenu(f_frame, options, "ID", "Name", "Type", "Author")
    f_options.pack(side=tk.LEFT)
    f_btn = tk.Button(f_frame, text="Find")
    f_btn.pack(side=tk.LEFT)
    f_frame.pack()
    # result frame
    book_list = ttk.Treeview(gui, columns=(1, 2, 3, 4), show="headings", height=8)
    book_list.heading(1, text='ID')
    book_list.heading(2, text='Name')
    book_list.heading(3, text='Type')
    book_list.heading(4, text="Author")
    book_list.pack()
    # book info
    info_frame = tk.Frame(gui)
    b_id = tk.Label(info_frame)
    b_name = tk.Label(info_frame)
    b_type = tk.Label(info_frame)
    b_author = tk.Label(info_frame)
    b_id.pack()
    b_name.pack()
    b_type.pack()
    b_author.pack()
    btn_frame = tk.Frame(info_frame)
    btn_frame.pack()
    read_btn = tk.Button(btn_frame, text="Read")
    dl_btn = tk.Button(btn_frame, text="Download")
    read_btn.pack(side=tk.LEFT, padx=10)
    dl_btn.pack(side=tk.LEFT, padx=10)
    info_frame.pack()

    def item_selected(event):
        for selected_item in book_list.selection():
            item = book_list.item(selected_item)
            record = item['values']
            read_btn.config(command=lambda: reader.read(record[0]))
            dl_btn.config(command=lambda: reader.donwload(record[0]))
            show_book_info(info_frame, record)

    book_list.bind('<<TreeviewSelect>>', item_selected)

    for i in range(0, 20):  # for dev
        book_list.insert('', tk.END, values=(f"CS{i}", f"Name{i}", "CS", f"Author{i}"))

    f_btn.config(command=lambda: find(book_list, f_content, f_options))
    gui.mainloop()


def find(list, content, option):
    req = {
        "type": "find",
        "content": content.get(),
        "option": option
    }

    # commute.send(req)
    # res = commute.recv()

    # update list
    list.delete(*list.get_children())


def show_book_info(f, record):
    e = f.winfo_children()
    e[0]["text"] = f"ID: {record[0]}"
    e[1]["text"] = f"Name: {record[1]}"
    e[2]["text"] = f"Type: {record[2]}"
    e[3]["text"] = f"Author: {record[3]}"
