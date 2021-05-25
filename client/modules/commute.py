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
    req_size = {"size": package.size()}
    print(req_size)
    req_size = json.dumps(req_size).encode()
    conn.sendall(req_size)  # send req size
    print(package)
    req = json.dumps(package).encode()
    conn.sendall(req)  # send req


def recv():
    res_size = conn.recv(128)  # recv res size
    res_size = json.loads(res_size.decode())
    print(res_size)
    res = conn.recv(res_size["size"])  # recv res
    res = json.loads(res.decode())
    print(res)
    return res
