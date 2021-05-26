import socket
import threading
import tkinter as tk

import modules.commute as commute
import modules.execute as execute


CLIENT_CONNECTION_MAX = 2
log = None


def create_connection(conn, addr):
    print("Connected by", addr)
    try:
        while True:
            try:
                req = commute.recv(conn)
                if req:
                    print(req)
                    execute.execute(conn, req)
            except Exception as e:
                print(e)
                break
    finally:
        conn.close()
        print("Disconnected by", addr)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 55555))
    server.listen(CLIENT_CONNECTION_MAX)
    print("Listening...")
    while server:
        try:
            conn, addr = server.accept()
            threading.Thread(target=create_connection, args=(conn, addr), daemon=True).start()
        except Exception:
            conn.close()


def build():
    global log
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
    dc_btn = tk.Button(l_f, text="Disconnect all", width=15, height=2, background="white", font=("Consolas", 15))
    dc_btn.pack(side=tk.LEFT, padx=20)
    port_lb = tk.Label(l_f, text="PORT: ", font=("Consolas", 15))
    port_lb.pack(side=tk.RIGHT, padx=20)
    l_f.pack(pady=10)

    log = tk.Text(gui)
    commute.set_log(log)
    log.pack(pady=10)
    gui.mainloop()
