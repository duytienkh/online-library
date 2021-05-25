import json
import socket
import threading


CLIENT_CONNECTION_MAX = 2
CLIENT_CONNECTION_COUNT = 0


def create_connection(conn, addr):
    global CLIENT_CONNECTION_COUNT
    if CLIENT_CONNECTION_COUNT + 1 <= CLIENT_CONNECTION_MAX:
        CLIENT_CONNECTION_COUNT += 1
    else:
        return
    print("Connected by", addr, "Current client count:", CLIENT_CONNECTION_COUNT)
    try:
        while True:
            try:
                req_size = conn.recv(128)
                req_size = json.loads(req_size.decode())
                print(req_size)
                req = conn.recv(req_size["size"])
                req = json.loads(req.decode())
                print(req)
            except Exception:
                break
    finally:
        print("Disconnected by", addr)
        conn.close()
        CLIENT_CONNECTION_COUNT -= 1


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 55555))
    server.listen()
    print("Listening...")
    while server:
        try:
            conn, addr = server.accept()
            threading.Thread(target=create_connection, args=(conn, addr), daemon=True).start()
        except Exception:
            conn.close()


if __name__ == "__main__":
    start_server()
