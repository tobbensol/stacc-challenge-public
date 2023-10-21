import datetime
from locale import currency
from random import randint
import Account
from Backend import Backend

class UserInterface:
    def __init__(self, backend: Backend):
        self.backend = backend

    def start(self):
        while True:
            choice = input("\n1. Add Account\n2. Make Transaction\n3. Plot Account Activity\n4. Quit\nEnter your choice: ")

            if choice == '1':
                account_data = self.get_account_data_from_user()
                self.backend.accounts.add_account(account_data)
                print(f"Successfully made account with the ID: {account_data['id']}")

            elif choice == '2':
                transaction_data = self.get_transaction_data_from_user()
                self.backend.make_transaction(transaction_data)

            elif choice == '3':
                account_id = input("Enter account ID: ")
                self.backend.plot_account_activity(account_id)

            elif choice == '4':
                break

    def get_transaction_data_from_user(self):
        # Implement code to get transaction data from the user (e.g., through input)
        id_str = str(randint(0, 999))
        id = "txn" + (3-len(id_str)) * "0" + id_str
        description = input("Description: ")
        amount = eval(input("Amount: ")) #TODO: safeEval
        currency = input("Currency: ")
        account_id = input("Account_ID: ")

        while True:
            date_str = input("Date (YYYY-MM-DD): ")
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                break  # Exit the loop if a valid date is provided
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        
        return({
            "id": id,
            "date": date,
            "description": description,
            "amount": amount,
            "currency": currency,
            "account_id": account_id
        })

    def get_account_data_from_user(self):
        # Implement code to get account data from the user (e.g., through input)
        id_str = str(randint(0, 999))
        id = "acc" + (3-len(id_str)) * "0" + id_str
        account_str = str(randint(0, 9999))
        account_number = "*"*8 + (4-len(account_str)) * "0" + account_str
        account_type = input("AccountType: ")
        balance = eval(input("Amount: ")) #TODO: safeEval
        currency = input("Currency: ")
        owner = input("Owner: ")
        
        return({
            "id": id,
            "account_number": account_number,
            "account_type": account_type,
            "balance": balance,
            "currency": currency,
            "owner": owner
        })