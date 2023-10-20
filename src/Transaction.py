from Account import Accounts
from tinydb import TinyDB, Query

class Transactions:
    def __init__(self, transactions: TinyDB.table_class):
        self.transactions: TinyDB.table_class = transactions

    def get_user_transaction(self, account_id: str):
        return self.transactions.search(Query().account_id == account_id)
        
    def get_transaction(self, id):
        return self.transactions.search(Query().id == id)
    
    def add_transactions(self, transaction: dict):
        self.transactions.insert(transaction)

    def __repr__(self):
        string = ""
        for i in self.transactions.all():
            string += str(i) + "\n"
        return string
    