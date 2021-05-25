import json
import socket
import sys
import xml.dom.minidom as minidom

conn = None


def create_connection():
    if not conn:
        doc = minidom.parse("config.xml")
        addr = doc.getElementsByTagName("address")[0].attributes["value"].value
        port = doc.getElementsByTagName("port")[0].attributes["value"].value
        connect(addr, int(port))


def connect(addr, port=55555):
    global conn
    try:
        print("Try to connect...")
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((addr, port))
        conn = sk
    except ConnectionRefusedError:
        print("show error msg")
        return


def send(package):
    if not conn:
        create_connection()
    req = json.dumps(package).encode()
    req_size = {"size": sys.getsizeof(req)}
    print(req_size)
    req_size = json.dumps(req_size).encode()
    conn.sendall(req_size)  # send req size
    print(package)
    conn.sendall(req)  # send req


def recv():
    res_size = conn.recv(128)  # recv res size
    res_size = json.loads(res_size.decode())
    print(res_size)
    res = conn.recv(res_size["size"])  # recv res
    res = json.loads(res.decode())
    print(res)
    return res
