import socket
import threading

import modules.commute as commute
import modules.execute as execute


CLIENT_CONNECTION_MAX = 2


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


if __name__ == "__main__":
    start_server()
