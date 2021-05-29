import base64

import modules.commute as commute

TO_KWARGS = {
    "ID": "book_id",
    "Name": "book_name",
    "Type": "book_type",
    "Author": "author",
    "Year": "year"
}


def execute(conn, req):
    import database.database as db
    req_type = req["type"]
    res = {
        "status": "",
        "data": "",
        "log": ""
    }
    if req_type == "sign_up":
        if db.check_user_exists(req["username"]) is True:
            res["status"] = False
            res["data"] = "username already existed"
            res["log"] = "Username was existed"
        else:
            res["status"] = db.create_account(req["username"], req["password"])
            res["data"] = "create unsuccessfully"
            res["log"] = "Error occurs when creating new account"
            if res["status"]:
                res["data"] = "create successfully"
                res["log"] = "A new account was created"
    if req_type == "sign_in":
        res["status"] = db.check_user_password(req["username"], req["password"])
        if res["status"]:
            res["log"] = "[" + req["username"] + "]" + " was signed in"
            commute.client_name_update(conn, req["username"])
        else:
            res["log"] = "Wrong username/password"
    if req_type == "find":
        content = req["content"]
        option = TO_KWARGS.get(req["option"])
        if option is None:
            books = []
        else:
            kwargs = {option: content}
            if len(content) == 0:
                kwargs = {}
            books = db.look_up_books(**kwargs)
        res["status"] = True
        res["data"] = books
        res["log"] = f"Books result was sent ({len(books)} books)"
    if req_type == "book_content":
        book_data = db.get_book_content(req["id"])
        if book_data is None:
            res["status"] = False
            res["log"] = f'Book (id: {req["id"]}) not found'
        else:
            res["data"], res["ext"] = book_data
            res["data"] = base64.b64encode(res["data"]).decode()
            res["log"] = f'Book (id: {req["id"]}) found, extension: {res["ext"]}'
            res["status"] = True
    if req_type == "disconnect":
        commute.disconnect(conn.getpeername(), conn)
        res["log"] = "Disconnected"
    commute.send(conn, res)
