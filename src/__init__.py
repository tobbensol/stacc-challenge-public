from user_interface import UserInterface
from bank.backend import Backend
from bank.transaction import Transactions
from bank.account import Accounts
from bank.saving_goal import Saving_goals

import json
from tinydb import TinyDB

# Load and delete DB
db = TinyDB("data/db.json")
db.drop_tables()

# Init tables
accounts = Accounts(db)
transactions = Transactions(db)
saving_goals = Saving_goals(db)

backend = Backend(accounts, transactions, saving_goals)
user_interface = UserInterface(backend)

# Load data from provided files
with open("data/accounts.json", "r") as f:
    contents = json.load(f)
    for i in contents["accounts"]:
        accounts.add_account(i)

with open("data/transactions.json", "r") as f:
    contents = json.load(f)
    for i in contents["transactions"]:
        backend.make_transaction(i)

with open("data/saving_goal.json", "r") as f:
    contents = json.load(f)
    for i in contents["transactions"]:
        pass

# Core program
if __name__ == "__main__":
    user_interface.start()
