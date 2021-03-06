import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import modules.commute as commute
import modules.reader as reader


def lib_gui(login_gui):
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
    r_frame = tk.Frame(gui)
    book_list_sb = tk.Scrollbar(r_frame)
    book_list_sb.pack(side=tk.RIGHT, fill='y')
    book_list = ttk.Treeview(r_frame, columns=(1, 2, 3, 4, 5), show="headings", yscrollcommand=book_list_sb.set)
    config_colum = [('ID', 10), ('Name', 250), ('Type', 90), ('Author', 110), ('Year', 50)]
    for num, col in enumerate(config_colum):
        name, width = col
        book_list.heading(num + 1, text=name)
        book_list.column(num + 1, width=width)
    book_list.pack()
    r_frame.pack(pady=10, padx=20)
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
    dcn_btn = tk.Button(gui, text="Disconnect", command=lambda: disconnect(login_gui, gui))
    dcn_btn.pack(side=tk.LEFT)

    def on_closing():
        commute.disconnect()
        gui.destroy()
        login_gui.destroy()
    gui.protocol("WM_DELETE_WINDOW", on_closing)
    gui.mainloop()


def disconnect(login_gui, lib_gui):
    if messagebox.askyesno("Are you sure?", "You must login again to reconnect to the server"):
        req = {
            "type": "disconnect",
            "log": "Send disconnect signal"
        }
        commute.send(req)
        commute.disconnect()
        lib_gui.destroy()
        login_gui.deiconify()


def find(book_list, content, option):
    req = {
        "type": "find",
        "content": content.get(),
        "option": option.get(),
        "log": "Find books"
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
