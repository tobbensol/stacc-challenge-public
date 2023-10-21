import random


def generate_random_int_str(prefix, length):
    id_int = str(random.randint(0, (10 ** length - 1)))
    return prefix + (length - len(id_int)) * "0" + id_int


def make_transaction(date: str, description: str, amount: float, account_id: str, currency: str = "NOK"):
    return {
        "id": generate_random_int_str("txn", 3),
        "date": date,
        "description": description,
        "amount": amount,
        "currency": currency,
        "account_id": account_id
    }


def make_account(account_type: str, balance: float, owner: str, currency: str = "NOK"):
    return ({
        "id": generate_random_int_str("acc", 3),
        "account_number": generate_random_int_str("*"*8, 4),
        "account_type": account_type,
        "balance": balance,
        "currency": currency,
        "owner": owner
    })


def make_savings_account(name: str, goal: float, current_amount: float, account_id: str, currency: str = "NOK"):
    return ({
        "id": generate_random_int_str("sav", 3),
        "name": name,
        "goal": goal,
        "current_amount": current_amount,
        "currency": currency,
        "account_id": account_id
    })