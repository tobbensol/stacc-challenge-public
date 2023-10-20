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
    
    def get_balance_history(self, account_id: str, transactions: TinyDB.table_class):
        #Gather info
        account = self.get_account(account_id)
        if not account:
            print("Account not found.")
            return None
        
        account_balance = account["balance"]
        transaction_data = transactions.search(Query().account_id == account_id)

        #Handle no transactions
        if not transaction_data: 
            #Should idealy be [account creation date, today]
            return [datetime.now()-timedelta(days=1), datetime.now()], [account_balance]*2
        
        #Handle dates
        sorted_transactions = sorted(transaction_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),)
        timestamps = [datetime.strptime(transaction["date"], "%Y-%m-%d") for transaction in sorted_transactions]
        before_first_transaction = timestamps[0] - timedelta(days=1)
        timestamps.insert(0, before_first_transaction)

        #Handle balances
        balances = [account_balance]
        for transaction in reversed(sorted_transactions):
            account_balance -= transaction["amount"]
            balances.insert(0, account_balance)
        
        return timestamps, balances

    def plot_account_activity(self, account_id: str, transactions: TinyDB.table_class):
        timestamps, balances = self.get_balance_history(account_id, transactions)

        #Linear regression
        days_since_first = [(date - timestamps[0]).days for date in timestamps]
        slope, intercept = np.polyfit(days_since_first, balances, 1)
        regression_line = slope * np.array(days_since_first) + intercept

        # Create a line chart to visualize the account balance over time
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, balances, marker='o')
        plt.plot(timestamps, regression_line, 'r-', label='Linear Regression Line')
        plt.title(f"Account Activity for Account ID {account_id}")
        plt.xlabel("Date")
        plt.ylabel("Account Balance (NOK)")
        plt.legend(["Balance", "Estimate"])
        plt.grid(True)

        # Display the chart or save it to a file
        plt.show()


    def __repr__(self):
        string = ""
        for i in self.accounts.all():
            string += str(i) + "\n"
        return string
