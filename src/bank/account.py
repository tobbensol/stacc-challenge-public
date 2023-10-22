from tinydb import TinyDB, Query
from tinydb.operations import add
from typing import Optional, List


class Accounts:
    def __init__(self, db: TinyDB):
        self.accounts: TinyDB.table_class = db.table("accounts")

    def change_balance(self, transaction: dict) -> Optional[List[int]]:
        amount = transaction["amount"]
        account_id = transaction["account_id"]
        if not self.accounts.get(Query().id == account_id):
            print("Could not find Account")
            return None

        if self.accounts.get(Query().id == account_id)["balance"] < -amount:
            print("Not enough available balance")
            return None

        return self.accounts.update(add("balance", amount), Query().id == account_id)

    def update_account(self, account_data: dict) -> None:
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
