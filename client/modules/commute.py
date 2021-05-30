import json
import os
import socket
import xml.dom.minidom as minidom
from tkinter import messagebox


class Disconnected(Exception):
    pass


conn = None


def create_connection():
    if not os.path.isfile("config.xml"):
        raise Exception("You should configure the server address first")
    doc = minidom.parse("config.xml")
    addr = doc.getElementsByTagName("address")[0].attributes["value"].value
    port = doc.getElementsByTagName("port")[0].attributes["value"].value
    s = connect(addr, int(port))
    if s:
        print("Connect successfully")
        return s
    print("Cant connect to server")
    return False


def connect(addr, port):
    global conn
    try:
        print("Try to connect...")
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(5)  # time out 5 seconds
        sk.connect((addr, port))
        conn = sk
    except Exception as e:
        print(e)
        conn = None
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
    try:
        print(len(req_size))
        conn.sendall(req_size)  # send req size
        print(package)
        conn.sendall(req)  # send req
        return True
    except Exception as e:
        messagebox.showerror("Disconnected", "Cannot connect to server. \n" + str(e))
        return False


def safe_recv(conn, size):
    resp = b''
    while len(resp) < size:
        part_resp = conn.recv(size - len(resp))
        if len(part_resp) == 0:
            raise ConnectionError
        resp += part_resp
    return resp


def recv():
    global conn
    res_size_b = safe_recv(conn, 128)  # recv res size
    res_size = None
    try:
        res_size = json.loads(res_size_b.decode())
    except Exception as e:
        print(e)
        print(res_size_b.decode())
        return
    print(res_size)
    resp_b = safe_recv(conn, res_size["size"])  # recv res
    resp = None
    try:
        resp = json.loads(resp_b.decode())
    except Exception as e:
        print(e)
        print(resp_b.decode()[:200], "...")
        return
    print(resp_b.decode()[:200], "...")
    return resp


def send_n_recv(package, auto_reconnect=False):
    global conn
    try:
        if send(package):
            return recv()
        else:
            if auto_reconnect:
                conn = None
    except Exception as e:
        messagebox.showerror("Disconnected", "Cannot connect to server. \n" + str(e))
        if auto_reconnect:
            conn = None
    return None
