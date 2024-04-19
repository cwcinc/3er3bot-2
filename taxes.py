import udata


def calculate_tax_percentage(user_id):
    user_balance = udata.getbal(user_id)
    if user_balance <= 0:
        return 0
    if user_balance <= 1000:
        return 1
    if user_balance <= 10000:
        return 2
    if user_balance <= 20000:
        return 3
    if user_balance <= 30000:
        return 4
    if user_balance <= 50000:
        return 5
    if user_balance <= 100000:
        return 8
    return 10


def tax_users(user_id_list):
    for user_id in user_id_list:
        percentage = calculate_tax_percentage(user_id) / 10
        print("Taxing user", user_id, "with", percentage, "%")
        udata.bank_transaction(user_id, -percentage)


def tax_all():
    tax_users(udata.getuserdata()["users"].keys())
