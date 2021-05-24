import tkinter as tk

import modules.commute as commute


def login_gui():
    gui = tk.Tk(className="login")
    # username frame
    u_frame = tk.Frame(gui)
    u_label = tk.Label(u_frame, text="username:")
    u_label.pack(side=tk.LEFT)
    u = tk.Entry(u_frame)
    u.pack(side=tk.RIGHT)
    u_frame.pack()
    # password frame
    p_frame = tk.Frame(gui)
    p_label = tk.Label(p_frame, text="password:")
    p_label.pack(side=tk.LEFT)
    p = tk.Entry(p_frame)
    p.pack(side=tk.RIGHT)
    p_frame.pack()
    # button frame
    btn_frame = tk.Frame(gui)
    sup_btn = tk.Button(btn_frame, text="sign up")
    sup_btn.pack(side=tk.LEFT, padx=10)
    sup_btn.config(command=lambda: sign_up(u, p))
    sin_btn = tk.Button(btn_frame, text="sign in")
    sin_btn.pack(side=tk.RIGHT, padx=10)
    sin_btn.config(command=lambda: sign_in(u, p))
    btn_frame.pack()
    gui.mainloop()


def sign_in(u, p):
    package = {
        "type": "sign_in",
        "username": u.get(),
        "password": p.get()
    }
    commute.send(package)


def sign_up(u, p):
    package = {
        "type": "sign_up",
        "username": u.get(),
        "password": p.get()
    }
    commute.send(package)
