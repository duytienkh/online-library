import json


def send(conn, package):
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


def recv(conn):
    res_size_b = conn.recv(128)  # recv res size
    if len(res_size_b) == 0:
        return None
    print(f"Received {len(res_size_b)} bytes")
    res_size = None
    try:
        res_size = json.loads(res_size_b.decode())
    except Exception as e:
        print(e)
        print(res_size_b)
        return
    print(res_size)
    resp_b = conn.recv(res_size["size"])  # recv res
    resp = None
    try:
        resp = json.loads(resp_b.decode())
    except Exception as e:
        print(e)
        print(f"Received {len(resp_b)} bytes")
        print(resp_b.decode())
        return
    print(resp)
    return resp