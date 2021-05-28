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
            res["log"] = "username was existed"
        else:
            res["status"] = db.create_account(req["username"], req["password"])
            res["data"] = "create unsuccessfully"
            res["log"] = "create unsuccessfully"
            if res["status"]:
                res["data"] = "create successfully"
                res["log"] = "account created"
    if req_type == "sign_in":
        res["status"] = db.check_user_password(req["username"], req["password"])
        if res["status"]:
            res["log"] = "signed in"
            commute.client_name_update(conn, req["username"])
        else:
            res["log"] = "couldnt sign in"
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
        res["log"] = f"books result was sent, found {len(books)} result"
    if req_type == "book_content":
        book_data = db.get_book_content(req["id"])
        if book_data is None:
            res["status"] = False
            res["log"] = f'Book id {req["id"]} not found'
        else:
            res["data"], res["ext"] = book_data
            res["data"] = base64.b64encode(res["data"]).decode()
            res["log"] = f'Book id {req["id"]} found, extension: {res["ext"]}'
            res["status"] = True
    commute.send(conn, res)
