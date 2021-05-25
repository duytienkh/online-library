import modules.commute as commute


def execute(conn, req):
    import database.database as db
    req_type = req["type"]
    res = {
        "status": "",
        "data": ""
    }
    if req_type == "sign_up":
        if db.check_user_exists(req["username"]) == True:
            res["status"] = False
            res["data"] = "username already existed"
        else:
            res["status"] = db.create_account(req["username"], req["password"])
            res["data"] = "create unsuccessfully"
            if res["status"]:
                res["data"] = "create successfully"
    if req_type == "sign_in":
        res["status"] = db.check_user_password(req["username"], req["password"])
    commute.send(conn, res)
