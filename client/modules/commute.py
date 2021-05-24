import json
import socket

conn = None


def connect(addr, port):
    global conn
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(addr, port)
        conn = sk
    except ConnectionRefusedError:
        print("show error msg")
        return


def send(package):
    req_size = json.dumps({"size": package.size()}).encode()
    conn.sendall(req_size)  # send req size
    req = json.dumps(package).encode()
    conn.sendall(req)  # send req


def recv():
    res_size = conn.recv(128)  # recv res size
    res_size = json.loads(res_size.decode())
    res = conn.recv(res_size["size"]).decode()  # recv res
    return res
