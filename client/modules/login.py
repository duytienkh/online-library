import tkinter as tk
from tkinter import messagebox

import modules.commute as commute
import modules.config as config
import modules.lib as lib


def login_gui():
    # gui
    gui = tk.Tk()
    gui.title("Login")
    gui.geometry("300x150")
    # username frame
    u_frame = tk.Frame(gui)
    u_label = tk.Label(u_frame, text="Username:")
    u_label.pack(side=tk.LEFT)
    u = tk.Entry(u_frame)
    u.pack(side=tk.RIGHT)
    u_frame.pack(pady=10)
    # password frame
    p_frame = tk.Frame(gui)
    p_label = tk.Label(p_frame, text="Password:")
    p_label.pack(side=tk.LEFT)
    p = tk.Entry(p_frame, show="*")
    p.pack(side=tk.RIGHT)
    p_frame.pack()
    # button frame
    btn_frame = tk.Frame(gui)
    cfg_btn = tk.Button(btn_frame, text="Configure")
    cfg_btn.pack(side=tk.LEFT, padx=10)
    cfg_btn.config(command=lambda: config.show(gui))
    sup_btn = tk.Button(btn_frame, text="Sign up")
    sup_btn.pack(side=tk.LEFT, padx=10)
    sup_btn.config(command=lambda: sign_up(u, p))
    sin_btn = tk.Button(btn_frame, text="Sign in")
    sin_btn.pack(side=tk.RIGHT, padx=10)
    sin_btn.config(command=lambda: sign_in(gui, u, p))
    btn_frame.pack(pady=30)

    def on_closing():
        commute.disconnect()
        gui.destroy()

    gui.protocol("WM_DELETE_WINDOW", on_closing)
    gui.mainloop()


def empty_check(u, p):
    if not u.get() or not p.get():
        messagebox.showerror("Errors", "Username or password must not empty")
        return True
    return False


def sign_in(gui, u, p):
    if empty_check(u, p):
        return
    req = {
        "type": "sign_in",
        "username": u.get(),
        "password": p.get(),
        "log": "Sign in"
    }
    resp = commute.send_n_recv(req, True)
    if resp:
        if resp["status"] is True:
            gui.withdraw()
            lib.lib_gui(gui)
        else:
            commute.disconnect()
            messagebox.showerror("", "Username/password was incorrect")
    else:
        commute.disconnect()


def sign_up(u, p):
    if empty_check(u, p):
        return
    req = {
        "type": "sign_up",
        "username": u.get(),
        "password": p.get(),
        "log": "Sign up"
    }
    resp = commute.send_n_recv(req, True)
    commute.disconnect()
    if resp:
        if resp["status"] is True:
            messagebox.showinfo("", "Successfully")
        else:
            messagebox.showerror("", "Error occurs: " + resp["data"])
