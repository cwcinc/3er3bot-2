import json


def getuserdata():
    with open("userdata.json", "r") as fp:
        userdata = json.load(fp)
    return userdata


def setuserdata(userdata):
    with open("userdata.json", "w") as fp:
        json.dump(userdata, fp)


def getbal(userid):
    userdata = getuserdata()
    return userdata["users"][str(userid)]


def setbal(userid, newbal):
    userdata = getuserdata()
    userdata["users"][str(userid)] = newbal
    setuserdata(userdata)


def changebal(userid, amount):
    userdata = getuserdata()
    userdata["users"][str(userid)] += amount
    setuserdata(userdata)


def bank_transaction(userid, percentage):
    """Positive percentage is paying the user from the bank
    Negative percentage is taxing the user to benefit the bank"""
    userdata = getuserdata()
    bank_balance = userdata["BANK"]
    payout = round(bank_balance * percentage / 100)

    try:
        userdata["users"][str(userid)] += payout
    except KeyError:
        print("Creating New User")
        userdata["users"][str(userid)] = payout

    userdata["BANK"] -= payout
    setuserdata(userdata)
    return payout
