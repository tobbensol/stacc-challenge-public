from tinydb import TinyDB, Query
from datetime import datetime, timedelta

class Transactions:
    def __init__(self, db: TinyDB):
        self.transactions: TinyDB.table_class = db.table("transactions")

    def get_balance_history(self, account_id: str):
        #Gather info
        change = 0
        transaction_data = self.get_user_transaction(account_id)

        #Handle no transactions
        if not transaction_data: 
            return [datetime.now().isoformat()-timedelta(days=1), datetime.now()], [change]*2
        
        #Handle dates
        sorted_transactions = sorted(transaction_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),)
        timestamps = [datetime.strptime(transaction["date"], "%Y-%m-%d") for transaction in sorted_transactions]
        before_first_transaction = timestamps[0] - timedelta(days=1)
        timestamps.insert(0, before_first_transaction)

        #Handle balances
        balances = [change]
        for transaction in reversed(sorted_transactions):
            change -= transaction["amount"]
            balances.insert(0, change)
        
        return timestamps, balances
    
    def add_transactions(self, transaction: dict):
        self.transactions.insert(transaction)

    def get_transaction(self, id):
        return self.transactions.search(Query().id == id)

    def get_user_transaction(self, account_id: str):
        return self.transactions.search(Query().account_id == account_id)

    def __repr__(self):
        string = ""
        for i in self.transactions.all():
            string += str(i) + "\n"
        return string
    