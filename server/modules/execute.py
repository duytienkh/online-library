import modules.commute as commute

TO_KWARGS = {
    "ID": "book_id",
    "Name": "book_name",
    "Type": "book_type",
    "Author": "author"
}


def execute(conn, req):
    import database.database as db
    req_type = req["type"]
    res = {
        "status": "",
        "data": ""
    }
    if req_type == "sign_up":
        if db.check_user_exists(req["username"]) is True:
            res["status"] = False
            res["data"] = "username already existed"
        else:
            res["status"] = db.create_account(req["username"], req["password"])
            res["data"] = "create unsuccessfully"
            if res["status"]:
                res["data"] = "create successfully"
    if req_type == "sign_in":
        res["status"] = db.check_user_password(req["username"], req["password"])
    if req_type == "find":
        content = req["content"]
        option = TO_KWARGS.get(req["option"])
        if option is None:
            res = []
        else:
            res = db.look_up_books(**{option: content})
    commute.send(conn, res)
