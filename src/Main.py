import json
from tinydb import TinyDB
from Account import Accounts
from Transaction import Transactions
from user_interface import UserInterface

# Load and delete DB
db = TinyDB("data/db.json")
db.drop_tables()

#Init tables
accounts = Accounts(db.table("accounts"))
transactions = Transactions(db.table("transactions"), accounts)

# Load data from provided files
with open("data/accounts.json", "r") as f:
    contents = json.load(f)
    for i in contents["accounts"]:
        accounts.add_account(i)

with open("data/transactions.json", "r") as f:
    contents = json.load(f)
    for i in contents["transactions"]:
        transactions.make_transaction(i)

# Core program
if __name__ == "__main__":
    user_interface = UserInterface(accounts, transactions)
    user_interface.start()
