from tinydb import TinyDB, Query
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

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

    def plot_account_activity(self, account_id: str, transactions: TinyDB.table_class):
        account = self.get_account(account_id)
        if not account:
            print("Account not found.")
            return

        account_balance = account["balance"]
        transaction_data = transactions.search(Query().account_id == account_id)

        if not transaction_data:
            print("No transactions found for this account.")
            return
        
        #Handle dates
        sorted_transactions = sorted(transaction_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
        timestamps = [transaction["date"] for transaction in sorted_transactions]
        before_first_transaction = datetime.strptime(timestamps[0], "%Y-%m-%d") - timedelta(days=1)
        timestamps.insert(0, before_first_transaction)

        #Handle balances
        balances = [account_balance]
        for transaction in transaction_data:
            account_balance -= transaction["amount"]
            balances.insert(0, account_balance)

        # Create a line chart to visualize the account balance over time
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, balances, marker='o')
        plt.title(f"Account Activity for Account ID {account_id}")
        plt.xlabel("Date")
        plt.ylabel("Account Balance (NOK)")
        plt.grid(True)

        # Display the chart or save it to a file
        plt.show()


    def __repr__(self):
        string = ""
        for i in self.accounts.all():
            string += str(i) + "\n"
        return string
