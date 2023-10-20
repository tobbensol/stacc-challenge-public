from tinydb import TinyDB
from Account import Accounts
from Transaction import Transactions

class UserInterface:
    def __init__(self, accounts: Accounts, transactions: Transactions):
        self.accounts: Accounts = accounts
        self.transactions: Transactions = transactions

    def start(self):
        while True:
            choice = input("1. Add Account\n2. Make Transaction\n3. Plot Account Activity\n4. Quit\nEnter your choice: ")

            if choice == '1':
                account_data = self.get_account_data_from_user()
                self.accounts.add_account(account_data)

            elif choice == '2':
                transaction_data = self.get_transaction_data_from_user()
                self.transactions.make_transaction(transaction_data)

            elif choice == '3':
                account_id = input("Enter account ID: ")
                self.accounts.plot_account_activity(account_id, self.transactions.transactions)

            elif choice == '4':
                break

    def get_account_data_from_user(self):
        # Implement code to get account data from the user (e.g., through input)
        pass

    def get_transaction_data_from_user(self):
        # Implement code to get transaction data from the user (e.g., through input)
        pass

    def make_transaction(self, transaction: dict) -> None:
        self.transactions.add_transactions(transaction)
        self.accounts.transaction(transaction)