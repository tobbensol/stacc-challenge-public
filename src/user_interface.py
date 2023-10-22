from src.bank.backend import Backend
import src.utils as utils

from datetime import datetime
from ast import literal_eval
from tinydb import TinyDB, Query


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
                    transaction_data = self.get_transaction_data_from_user()
                    self.backend.make_transaction(transaction_data)
                case "3":
                    account_id = get_id_from_user(self.backend.accounts.accounts, "Enter account ID: ")
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
3. Change monthly payment
4. Make monthly payments
5. Plot estimates
6. Quit\n
Enter your choice: 
""")
            match choice:
                case "1":
                    savings_data = self.get_savings_account_from_user()
                    self.backend.saving_goals.add_saving_goal(savings_data)
                    print(f"Successfully made savings account with the ID: {savings_data['id']}")
                case "2":
                    savings_account, transaction = self.get_savings_transfer_from_user()
                    self.backend.transfer_to_savings(savings_account, transaction)
                case "3":
                    account_id = get_id_from_user(self.backend.saving_goals.saving_goals, "Enter savings ID: ")
                    monthly_payment = get_numeric_from_user("Enter new monthly payment: ")
                    self.backend.saving_goals.set_monthly_payment(account_id, monthly_payment)
                case "4":
                    date = get_date_from_user()
                    self.backend.make_monthly_saving(date)
                case "5":
                    account_id = get_id_from_user(self.backend.saving_goals.saving_goals, "Enter savings ID: ")
                    self.backend.saving_goals.plot_saving_goal(account_id)
                case "6":
                    break
                case _:
                    print("Please enter a valid option")

    def get_transaction_data_from_user(self):
        description = input("Description: ")
        amount = get_numeric_from_user("Amount: ")
        account_id = get_id_from_user(self.backend.accounts.accounts, "Enter account ID: ")
        date = get_date_from_user()

        return utils.make_transaction(date, description, amount, account_id)

    def get_savings_account_from_user(self):
        name = input("What are you saving for? ")
        goal = get_numeric_from_user("How much does is cost? ")
        account_id = get_id_from_user(self.backend.accounts.accounts, "Enter account ID: ")
        return utils.make_savings_account(name, goal, 0, account_id)

    def get_savings_transfer_from_user(self):
        savings_id = get_id_from_user(self.backend.saving_goals.saving_goals, "Enter savings ID: ")
        amount = get_numeric_from_user("Amount: ")
        description = f"Savings transfer to {savings_id}"
        date = get_date_from_user()
        account_id = self.backend.saving_goals.get_saving_goal(savings_id)["account_id"]

        return savings_id, utils.make_transaction(date, description, amount, account_id)


def get_account_data_from_user():
    account_type = input("AccountType: ")
    owner = input("Owner: ")
    return utils.make_account(account_type, 0, owner)


def get_date_from_user() -> str:
    while True:
        # Check if input is valid
        try:
            date = datetime.strptime(input("Date (YYYY-MM-DD): "), "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    return date.strftime("%Y-%m-%d")


def get_numeric_from_user(input_str: str) -> float:
    while True:
        # Check if input is valid
        try:
            value = literal_eval(input(input_str))
            break
        except ValueError:
            print("Invalid Number. Please enter a number")
    return value


def get_id_from_user(table: TinyDB.table_class, input_str: str) -> str:
    while True:
        table_id = input(input_str)
        if table.contains(Query().id == table_id):
            break
        else:
            print("Invalid ID. Please enter a valid ID")
    return table_id
