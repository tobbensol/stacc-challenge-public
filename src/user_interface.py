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
6. Quit\n
Enter your choice: 
""")
            match choice:
                case "1":  # Add Account
                    account_data = get_account_data_from_user()
                    self.backend.accounts.add_account(account_data)
                    print(f"Successfully made {account_data['account_type']} account with the ID: {account_data['id']}")
                case "2":  # Make Transaction
                    transaction_data = self.get_transaction_data_from_user()
                    if self.backend.make_transaction(transaction_data):
                        print("Transaction was successful!")
                case "3":  # Plot Account Activity
                    account_id = get_id_from_user(self.backend.accounts.accounts, "Enter account ID: ")
                    self.backend.plot_account_activity(account_id)
                case "4":  # Manage Savings
                    self.savings()
                case "5":  # Print DB
                    print(self.backend)
                case "6":  # Quit
                    break
                case _:
                    print("Please enter a valid option")

    def savings(self):
        while True:
            choice = input("""
1. Add savings account
2. Transfer to savings account
3. Plot estimates
4. Change monthly payment
5. Make monthly payments
6. See saving accounts
7. Quit\n
Enter your choice: 
""")
            match choice:
                case "1":  # Add savings account
                    savings_data = self.get_savings_account_from_user()
                    self.backend.saving_goals.add_saving_goal(savings_data)
                    print(
                        f"Successfully made savings account for \"{savings_data['name']}\" with the ID: {savings_data['id']}")
                case "2":  # Transfer to savings account
                    savings_account, transaction = self.get_savings_transfer_from_user()
                    self.backend.transfer_to_savings(savings_account, transaction)
                case "3":  # Plot estimates
                    account_id = get_id_from_user(self.backend.saving_goals.saving_goals, "Enter savings ID: ")
                    end_date = self.backend.saving_goals.plot_saving_goal(account_id)
                    print(f"Estimated to be done by: {end_date}")
                case "4":  # Change monthly payment
                    account_id = get_id_from_user(self.backend.saving_goals.saving_goals, "Enter savings ID: ")
                    monthly_payment = get_numeric_from_user("Enter new monthly payment: ", True)
                    self.backend.saving_goals.set_monthly_payment(account_id, monthly_payment)
                case "5":  # Make monthly payments
                    date = get_date_from_user()
                    self.backend.make_monthly_saving(date)
                case "6":  # See saving accounts
                    account_id = get_id_from_user(self.backend.accounts.accounts, "Enter account ID: ")
                    accounts = self.backend.saving_goals.get_user_saving_goals(account_id)
                    if accounts:
                        print(self.saving_to_str(account_id, accounts))
                    else:
                        print(f"{account_id} has no saving accounts tied to it")
                case "7":  # Quit
                    break
                case _:
                    print("Please enter a valid option")

    def get_transaction_data_from_user(self):
        description = input("Description: ")
        amount = get_numeric_from_user("Amount: ", False)
        account_id = get_id_from_user(self.backend.accounts.accounts, "Enter account ID: ")
        date = get_date_from_user()

        return utils.make_transaction(date, description, amount, account_id)

    def get_savings_account_from_user(self):
        name = input("What are you saving for? ")
        goal = get_numeric_from_user("How much does is cost? ", True)
        account_id = get_id_from_user(self.backend.accounts.accounts, "Enter account ID: ")
        return utils.make_savings_account(name, goal, 0, 0, account_id)

    def get_savings_transfer_from_user(self):
        savings_id = get_id_from_user(self.backend.saving_goals.saving_goals, "Enter savings ID: ")
        amount = get_numeric_from_user("Amount: ", True)
        description = f"Savings transfer to {savings_id}"
        date = get_date_from_user()
        account_id = self.backend.saving_goals.get_saving_goal(savings_id)["account_id"]

        return savings_id, utils.make_transaction(date, description, -amount, account_id)

    def saving_to_str(self, account_id, accounts) -> str:
        output = f"{account_id}'s saving accounts:"
        for i in accounts:
            output += f"""
id: {i["id"]}
name: {i["name"]}
progress: {i["current_amount"]}{i["currency"]}/{i["goal"]}{i["currency"]} = {self.backend.saving_goals.check_saving_goal_progress(i["id"]) * 100}%
monthly payment = {i["monthly_payment"]}
main account = {i["account_id"]}
"""
        return output


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


def get_numeric_from_user(input_str: str, positive: bool) -> float:
    while True:
        # Check if input is valid
        try:
            value_str = input(input_str)
            value = literal_eval(value_str)
            # breaks if
            if positive and value < 0:
                print("Please enter a positive number")
            else:
                break
        except:
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
