from tinydb import TinyDB, Query
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import numpy as np

class Accounts():
    def __init__(self, accounts: TinyDB.table_class):
        self.accounts: TinyDB.table_class = accounts
    
    def transaction(self, transaction: dict) -> None:
        amount = transaction["amount"]
        account_id = transaction["account_id"]
        account = self.get_account(account_id)
        if account:
            account["balance"] = account.get("balance", 0) + amount
            self.update_account(account)

    def update_account(self, account_data: dict):
        account_id = account_data["id"]
        self.accounts.update(account_data, Query().id == account_id)

    def add_account(self, account: dict) -> None:
        self.accounts.insert(account)
    
    def remove_account(self, account_id: str) -> None:
        self.accounts.remove(Query().id == account_id)

    def get_account(self, account_id: str):
        return self.accounts.get(Query().id == account_id)

    def __repr__(self):
        string = ""
        for i in self.accounts.all():
            string += str(i) + "\n"
        return string
