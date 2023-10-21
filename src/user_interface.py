from src.bank.backend import Backend
import src.utils as utils

from datetime import datetime
from ast import literal_eval
import random


class UserInterface:
    def __init__(self, backend: Backend):
        self.backend = backend

    def start(self):
        while True:
            choice = input("""
1. Add Account
2. Make Transaction
3. Plot Account Activity
4. Manage Savings
5. Print DB
5. Quit\n
Enter your choice: 
""")
            match choice:
                case "1":
                    account_data = get_account_data_from_user()
                    self.backend.accounts.add_account(account_data)
                    print(f"Successfully made account with the ID: {account_data['id']}")
                case "2":
                    transaction_data = get_transaction_data_from_user()
                    self.backend.make_transaction(transaction_data)
                case "3":
                    account_id = input("Enter account ID: ")
                    self.backend.plot_account_activity(account_id)
                case "4":
                    self.savings()
                case "5":
                    print(self.backend)
                case "6":
                    break
                case _:
                    print("Please enter a valid option")

    def savings(self):
        while True:
            choice = input("""
1. Add savings account
2. Transfer to savings account
3. Make monthly payments
4. Plot estimates
5. Quit\n
Enter your choice: 
""")
            match choice:
                case "1":
                    savings_data = get_savings_account_from_user()
                    self.backend.saving_goals.add_saving_goal(savings_data)
                case "2":
                    savings_account, transaction = get_savings_transfer_from_user()
                    self.backend.transfer_to_savings(savings_account, transaction)
                case "3":
                    self.backend.make_monthly_saving()
                case "4":
                    pass
                case "5":
                    break
                case _:
                    print("Please enter a valid option")
            print(self.backend.saving_goals)


def get_transaction_data_from_user():
    description = input("Description: ")
    amount = literal_eval(input("Amount: "))
    account_id = input("Account_ID: ")

    while True:
        date_str = input("Date (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            break  # Exit the loop if a valid date is provided
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    return utils.make_transaction(date.strftime("%Y-%m-%d"), description, amount, account_id)


def get_account_data_from_user():
    account_type = input("AccountType: ")
    owner = input("Owner: ")
    return utils.make_account(account_type, 0, owner)


def get_savings_account_from_user():
    name = input("What are you saving for? ")
    goal = " "
    while not goal.isnumeric():
        goal = input("How much does is cost? ")
    account = input("Which account is this tied to? ")
    return utils.make_savings_account(name, float(goal), 0, account)


def get_savings_transfer_from_user():
    savings_id = input("Savings ID: ")
    amount = literal_eval(input("Amount: "))
    description = f"Savings transfer to {savings_id}"

    while True:
        date_str = input("Date (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            break  # Exit the loop if a valid date is provided
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    return savings_id, utils.make_transaction(date.strftime("%Y-%m-%d"), description, amount, "temp")
