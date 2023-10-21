from tinydb import TinyDB, Query
from tinydb.operations import add


class Accounts:
    def __init__(self, db: TinyDB):
        self.accounts: TinyDB.table_class = db.table("accounts")

    def change_balance(self, transaction: dict) -> None:
        amount = transaction["amount"]
        account_id = transaction["account_id"]
        self.accounts.update(add("balance", amount), Query().id == account_id)

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
