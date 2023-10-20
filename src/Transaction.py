from Account import Accounts
from tinydb import TinyDB, Query

class Transactions:
    def __init__(self, transactions: TinyDB.table_class, accounts: Accounts):
        self.transactions: TinyDB.table_class = transactions
        self.accounts: Accounts = accounts

    def make_transaction(self, transaction: dict) -> None:
        self.transactions.insert(transaction)
        self.accounts.transaction(transaction)

    def __repr__(self):
        string = ""
        for i in self.transactions.all():
            string += str(i) + "\n"
        return string
    