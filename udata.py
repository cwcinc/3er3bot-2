import json


def getuserdata():
    with open("userdata.json", "r") as fp:
        userdata = json.load(fp)
    return userdata


def setuserdata(userdata):
    with open("userdata.json", "w") as fp:
        json.dump(userdata, fp)


def getbal(userid):
    try_new_user(userid)
    userdata = getuserdata()
    return userdata["users"][str(userid)]["bal"]


def setbal(userid, newbal):
    try_new_user(userid)
    userdata = getuserdata()
    userdata["users"][str(userid)]["bal"] = newbal
    setuserdata(userdata)


def changebal(userid, amount):
    try_new_user(userid)
    userdata = getuserdata()
    userdata["users"][str(userid)]["bal"] += amount
    setuserdata(userdata)


def try_new_user(userid, balance=0, betting=False):
    userdata = getuserdata()
    user = userdata["users"].get(str(userid), None)
    if user is not None:
        return

    new_user = {"bal": balance, "is_betting": betting}
    userdata["users"][str(userid)] = new_user
    setuserdata(userdata)


def bank_transaction(userid, percentage):
    """Positive percentage is paying the user from the bank
    Negative percentage is taxing the user to benefit the bank"""

    try_new_user(userid)
    userdata = getuserdata()
    bank_balance = userdata["BANK"]
    payout = round(bank_balance * percentage / 100)

    userdata["users"][str(userid)]["bal"] += payout

    userdata["BANK"] -= payout
    setuserdata(userdata)
    return payout


def is_betting(userid):
    try_new_user(userid)
    userdata = getuserdata()
    return userdata["users"][str(userid)]["is_betting"]


def set_betting(userid, status):
    try_new_user(userid)
    userdata = getuserdata()
    userdata["users"][str(userid)]["is_betting"] = status
    setuserdata(userdata)
