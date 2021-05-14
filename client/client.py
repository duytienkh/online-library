import socket
import time


def connect_server(server_address):
    print("Try to connect server", server_address)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(server_address)

    return conn


if __name__ == "__main__":
    conn = connect_server(("127.0.0.1", 55555))
    conn.close()
