from src.bank.account import Accounts
from src.bank.transaction import Transactions
from src.bank.saving_goal import SavingGoals
import src.utils as utils

from matplotlib import pyplot as plt
from typing import Tuple, List, Optional
from datetime import datetime
import numpy as np


class Backend:
    def __init__(self, accounts: Accounts, transactions: Transactions, saving_goals: SavingGoals):
        self.accounts: Accounts = accounts
        self.transactions: Transactions = transactions
        self.saving_goals: SavingGoals = saving_goals

    def make_transaction(self, transaction: dict) -> bool:
        if self.accounts.change_balance(transaction):
            self.transactions.add_transactions(transaction)
            return True
        return False

    def get_balance_history(self, account_id: str) -> Tuple[Optional[List[datetime]], Optional[List[int]]]:
        account = self.accounts.get_account(account_id)
        if not account:
            print("Account not found.")
            return None, None
        account_balance = account["balance"]
        date, change = self.transactions.get_balance_history(account_id)

        return date, [account_balance + x for x in change]

    def transfer_to_savings(self, savings_id: str, transaction: dict) -> None:
        if not self.make_transaction(transaction):
            return
        progress = self.saving_goals.change_balance(savings_id, -transaction["amount"])
        if progress >= 1:
            savings_account = self.saving_goals.get_saving_goal(savings_id)
            return_transaction = utils.make_transaction(
                str(datetime.now()),  # Use the current date
                "Return from savings",
                savings_account["goal"] * progress,
                savings_account["account_id"],
                savings_account["currency"]
            )
            # return money, and delete goal
            if not self.make_transaction(return_transaction):
                return
            self.saving_goals.remove_saving_goal(savings_id)
            print(f"You have saved up for \"{savings_account['name']}\", the money has been returned to your account!")

    def plot_account_activity(self, account_id: str) -> None:
        timestamps, balances = self.get_balance_history(account_id)
        if not timestamps or not balances:
            return

        # Linear regression
        days_since_first = [(date - timestamps[0]).days for date in timestamps]
        slope, intercept = np.polyfit(days_since_first, balances, 1)
        regression_line = slope * np.array(days_since_first) + intercept

        # Create a line chart to visualize the account balance over time
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, balances, drawstyle="steps-post", marker="o")
        plt.plot(timestamps, regression_line, "r-", label="Linear Regression Line")
        plt.title(f"Account Activity for Account ID {account_id}")
        plt.xlabel("Date")
        plt.ylabel("Account Balance (NOK)")
        plt.legend(["Balance", "Estimate"])
        plt.grid(True)

        # Display the chart or save it to a file
        plt.show()

    def make_monthly_saving(self, date) -> None:
        goals = self.saving_goals.saving_goals.all()
        for goal in goals:
            account = self.accounts.get_account(goal["account_id"])
            monthly_payment = goal["monthly_payment"]

            if not account:
                print("Account not found.")
                return

            if account["balance"] >= monthly_payment:
                # Deduct the monthly payment from the account
                transaction = utils.make_transaction(date,
                                                     f"Monthly payment for {goal['name']}",
                                                     -monthly_payment,
                                                     goal["account_id"]
                                                     )
                self.transfer_to_savings(goal["id"], transaction)

    def __repr__(self):
        return (f"Accounts:\n{self.accounts}\n" +
                f"Transactions:\n{self.transactions}\n" +
                f"Saving Goals\n{self.saving_goals}")
