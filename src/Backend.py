from account import Accounts
from transaction import Transactions

from matplotlib import pyplot as plt
import numpy as np

class Backend():
    def __init__(self, accounts: Accounts, transactions: Transactions):
        self.accounts: Accounts = accounts
        self.transactions: Transactions = transactions

    def make_transaction(self, transaction: dict) -> None:
        self.transactions.add_transactions(transaction)
        self.accounts.transaction(transaction)

    def get_balance_history(self, account_id: str):
        account = self.accounts.get_account(account_id)
        if not account:
            print("Account not found.")
            return None
        account_balance = account["balance"]
        date, change = self.transactions.get_balance_history(account_id)

        return date, [account_balance + x for x in change]

    def plot_account_activity(self, account_id: str):
        balance_history = self.get_balance_history(account_id)
        if not balance_history:
            return
        
        timestamps, balances = balance_history

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