import json
import socket
import xml.dom.minidom as minidom
from tkinter import messagebox


class Disconnected(Exception):
    pass


conn = None


def create_connection():
    if not conn:
        doc = minidom.parse("config.xml")
        addr = doc.getElementsByTagName("address")[0].attributes["value"].value
        port = doc.getElementsByTagName("port")[0].attributes["value"].value
        s = connect(addr, int(port))
        if s:
            print("Connect successfully")
        else:
            print("Cant connect to server")
        return s
    return True


def connect(addr, port=55555):
    global conn
    try:
        print("Try to connect...")
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((addr, port))
        conn = sk
    except Exception as e:
        print(e)
        return False
    return True


def disconnect():
    global conn
    if not conn:
        return
    print("Disconnected")
    conn.close()
    conn = None


def send(package):
    global conn
    if not conn:
        if not create_connection():
            raise Disconnected
    req = json.dumps(package).encode()
    req_size = {"size": len(req)}
    print(req_size)
    req_size = json.dumps(req_size).encode()
    while len(req_size) < 128:
        req_size += b" "
    print(len(req_size))
    conn.sendall(req_size)  # send req size
    print(package)
    conn.sendall(req)  # send req


def recv():
    global conn
    res_size_b = conn.recv(128)  # recv res size
    res_size = None
    try:
        res_size = json.loads(res_size_b.decode())
    except Exception as e:
        print(e)
        print(res_size_b.decode())
        return
    print(res_size)
    resp_b = conn.recv(res_size["size"])  # recv res
    resp = None
    try:
        resp = json.loads(resp_b.decode())
    except Exception as e:
        print(e)
        print(resp_b.decode()[:200], "...")
        return
    print(resp_b.decode()[:200], "...")
    return resp


def send_n_recv(package):
    try:
        send(package)
        return recv()
    except Exception as e:
        messagebox.showerror("Disconnected", "Cannot connect to server. \n" + str(e))
    return None
