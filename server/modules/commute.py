import json
import tkinter as tk

CLIENT_CONNECTION = 0
CLIENT_CONNECTION_MAX = 0

log = None
clients = {}


def client_name_update(conn, name):
    addr = conn.getpeername()
    clients[addr[0] + " " + str(addr[1])]["name"] = name


def add_client(addr, conn):
    client_key = addr[0] + " " + str(addr[1])
    clients[client_key] = {
        "name": "(" + addr[0] + ", " + str(addr[1]) + ")",
        "conn": conn,
        "addr": addr,
    }


def log_push(msg):
    log["state"] = tk.NORMAL
    log.insert("0.0", "\n" + msg)
    log["state"] = tk.DISABLED


def disconnect(addr, conn):
    global CLIENT_CONNECTION
    client_key = addr[0] + " " + str(addr[1])
    if client_key in clients:
        clients.pop(client_key)
        conn.close()
        print(f"{addr} has disconnected")
        log_push(f"--- {addr} has disconnected ---")
        CLIENT_CONNECTION -= 1


def disconnect_all():
    cur_clients = [c for _, c in clients.items()]
    for c in cur_clients:
        disconnect(c["addr"], c["conn"])


def set_log(log_value):
    global log
    log = log_value
    # addr = addr_value


def log_update(f):
    global log

    def wrapper(*args, **kw):
        package = f(*args, **kw)
        addr = args[0].getpeername()
        c_name = clients[addr[0] + " " + str(addr[1])]["name"]
        direct = " <-- " if f.__name__ == "send" else " --> "
        log_push(c_name + direct + package["log"])
        return package

    return wrapper


@log_update
def send(conn, package):
    req = json.dumps(package).encode()
    req_size = {"size": len(req)}
    print(req_size)
    req_size = json.dumps(req_size).encode()
    if len(req_size) < 128:
        req_size += b" " * (128 - len(req_size))

    conn.sendall(req_size)  # send req size
    conn.sendall(req)  # send req
    return package


def safe_recv(conn, size):
    resp = b''
    while len(resp) < size:
        part_resp = conn.recv(size - len(resp))
        if len(part_resp) == 0:
            raise ConnectionError
        resp += part_resp
    return resp


@log_update
def recv(conn):
    res_size_b = safe_recv(conn, 128)  # recv res size

    if len(res_size_b) == 0:
        raise ConnectionError
    res_size = None
    try:
        res_size = json.loads(res_size_b.decode())
    except Exception as e:
        print("Error:", e)
        print("Detail:", res_size_b)
        raise RuntimeError

    resp_b = safe_recv(conn, res_size["size"])  # recv res
    resp = None
    try:
        resp = json.loads(resp_b.decode())
    except Exception as e:
        print("Error:", e)
        print("Detail:", resp_b.decode())
        raise RuntimeError

    return resp
