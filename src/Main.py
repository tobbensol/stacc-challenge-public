import json
from tinydb import TinyDB, Query
from Account import Accounts
from Transaction import Transactions

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
print(accounts)

accounts.add_account(
    {
    "id": "acc222",
      "account_number": "********5121",
      "account_type": "Savings",
      "balance": 4000.0,
      "currency": "NOK",
      "owner": "Tobias"
    }
)

accounts.plot_account_activity("acc123", transactions.transactions)
