import json
import tkinter as tk

log = None


def set_log(log_value):
    global addr, log
    log = log_value
    # addr = addr_value


def log_push(msg):
    log["state"] = tk.NORMAL
    log.insert("0.0", "\n" + msg)
    log["state"] = tk.DISABLED


def log_update(f):
    global log

    def wrapper(*args, **kw):
        package = f(*args, **kw)
        c_ip = args[0].getpeername()[0]
        direct = " <-- " if f.__name__ == "send" else " --> "
        log_push(c_ip + direct + package["log"])
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


@log_update
def recv(conn):
    res_size_b = conn.recv(128)  # recv res size

    if len(res_size_b) == 0:
        raise ConnectionError
    res_size = None
    try:
        res_size = json.loads(res_size_b.decode())
    except Exception as e:
        print("Error:", e)
        print("Detail:", res_size_b)
        raise RuntimeError

    resp_b = conn.recv(res_size["size"])  # recv res
    resp = None
    try:
        resp = json.loads(resp_b.decode())
    except Exception as e:
        print("Error:", e)
        print("Detail:", resp_b.decode())
        raise RuntimeError

    return resp
