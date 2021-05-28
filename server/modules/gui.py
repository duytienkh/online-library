import socket
import threading
import tkinter as tk
from tkinter import messagebox

import modules.commute as commute
import modules.execute as execute


class customSocket(socket.socket):
    is_None = False

    def set_to_none(self):
        self.is_None = True


conn_cnt = None
l_btn = None
log = None


def create_connection(conn, addr):
    commute.CLIENT_CONNECTION += 1
    print(f"{addr} has connected")
    commute.log_push(f"+++ {addr} has connected +++")
    commute.add_client(addr, conn)
    try:
        while True:
            try:
                req = commute.recv(conn)
                if req:
                    print(req)
                    execute.execute(conn, req)
            except Exception as e:
                print("Error:", e)
                break
    finally:
        commute.disconnect(addr, conn)


def close_server(server):
    global l_btn
    commute.disconnect_all()
    server.close()
    server.set_to_none()
    l_btn["text"] = "Launch"
    l_btn.config(command=lambda: threading.Thread(target=start_server, args=(), daemon=True).start())
    commute.log_push("=== Server has been closed ===")


def start_server():
    global l_btn
    try:
        commute.CLIENT_CONNECTION_MAX = int(conn_cnt.get())
        commute.CLIENT_CONNECTION = 0
        if commute.CLIENT_CONNECTION_MAX <= 0:
            raise Exception("CONNECTION_MAX should larger than 0")
    except Exception as e:
        print(e)
        messagebox.showerror("Server error", "Max connection is invalid")
        raise RuntimeError
    server = customSocket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 55555))
    server.listen()
    commute.log_push("=== Server is listening on port 55555 ===")
    # change launch button to close
    l_btn["text"] = "Close"
    l_btn.config(command=lambda: close_server(server))
    while server and not server.is_None:
        conn = None
        try:
            conn, addr = server.accept()
            if commute.CLIENT_CONNECTION == commute.CLIENT_CONNECTION_MAX:
                commute.log_push(f"### Rejected {addr} because of enough connections")
                raise Exception("Enough connections")
            threading.Thread(target=create_connection, args=(conn, addr), daemon=True).start()
        except Exception:
            if conn is not None:
                conn.close()


def build():
    global conn_cnt, l_btn, log
    gui = tk.Tk()
    gui.title("Online-Library Server")
    gui.geometry("600x500")
    tk.Label(
        master=gui,
        text="Online-Library Server",
        font=("Consolas", 30),
        # borderwidth=5, relief="solid"
    ).pack(
        anchor=tk.CENTER,
        pady=20,
        padx=20
    )

    l_f = tk.Frame(gui)
    l_btn = tk.Button(l_f, text="Launch", width=10, height=2, background="white", font=("Consolas", 15))
    l_btn.pack(side=tk.LEFT, padx=20)
    l_btn.config(command=lambda: threading.Thread(target=start_server, args=(), daemon=True).start())
    cnt_f = tk.Frame(l_f)
    cnt_lb = tk.Label(cnt_f, text="Max connection", font=("Consolas", 12))
    cnt_lb.pack()
    cnt_ent = tk.Entry(cnt_f)
    cnt_ent.insert(tk.END, 2)
    cnt_ent.pack()
    conn_cnt = cnt_ent
    cnt_f.pack(side=tk.LEFT)
    dc_btn = tk.Button(l_f, text="Disconnect all", width=15, height=2, background="white", font=("Consolas", 15))
    dc_btn.pack(side=tk.LEFT, padx=20)
    dc_btn.config(command=lambda: threading.Thread(target=commute.disconnect_all(), args=(), daemon=True).start())
    l_f.pack(pady=10)

    log = tk.Text(gui, font=("Consolas", 10), state=tk.DISABLED)
    commute.set_log(log)
    log.pack(pady=10)
    gui.mainloop()
