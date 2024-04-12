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
    return userdata[str(userid)]


def setbal(userid, newbal):
    userdata = getuserdata()
    userdata[str(userid)] = newbal
    setuserdata(userdata)


def changebal(userid, amount):
    userdata = getuserdata()
    userdata[str(userid)] += amount
    setuserdata(userdata)