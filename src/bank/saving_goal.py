from tinydb import TinyDB, Query
from tinydb.operations import add
from matplotlib import pyplot as plt
from datetime import datetime, timedelta


class SavingGoals:
    """
    very similar to a normal account
    ID: int
    Name: Str
    Goal: int
    Current_Amount: int
    Currency: str
    account_id: int
    """

    def __init__(self, db: TinyDB):
        self.saving_goals: TinyDB.table_class = db.table("saving_goals")

    def change_balance(self, savings_id: str, amount: float) -> None:
        self.saving_goals.update(add("current_amount", amount), Query().id == savings_id)

    def check_saving_goal_progress(self, savings_id: str) -> float:
        saving_goal = self.get_saving_goal(savings_id)
        if not saving_goal:
            return 0

        current_balance = saving_goal.get("balance", 0)
        goal = saving_goal.get("saving_goal", 0)

        if current_balance >= goal:
            return 100  # 100% progress if the goal is achieved
        else:
            return (current_balance / goal) * 100

    def plot_saving_goal(self, savings_id: str) -> None:
        saving_goal = self.get_saving_goal(savings_id)
        if not saving_goal:
            print("Saving goal not found.")
            return

        current_amount = saving_goal["current_amount"]
        goal = saving_goal["goal"]
        monthly_payment = saving_goal["monthly_payment"]

        if current_amount >= goal:
            print("Congratulations! You have already reached your saving goal.")
            return

        months = 0
        savings_progress = [current_amount]
        date = datetime.now()
        x = [date]

        while current_amount < goal:
            current_amount += monthly_payment
            if current_amount > goal:
                current_amount = goal
            months += 1
            date += timedelta(days=30)  # Approximating a month with 30 days
            x.append(date)
            savings_progress.append(current_amount)

        plt.plot(x, savings_progress, label="Savings Progress")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Saving Goal Progress")
        plt.axhline(y=goal, color="r", linestyle="--", label="Goal")
        plt.legend()
        plt.grid()

        plt.show()

    def set_monthly_payment(self, savings_id: str, amount: float) -> None:
        self.saving_goals.update({"monthly_payment": amount}, Query().id == savings_id)

    def add_saving_goal(self, account: dict) -> None:
        self.saving_goals.insert(account)

    def remove_saving_goal(self, savings_id: str) -> None:
        self.saving_goals.remove(Query().id == savings_id)

    def get_saving_goal(self, savings_id: str):
        return self.saving_goals.get(Query().id == savings_id)

    def get_user_saving_goals(self, savings_id: str):
        return self.saving_goals.search(Query().account_id == savings_id)

    def __repr__(self):
        string = ""
        for i in self.saving_goals.all():
            string += str(i) + "\n"
        return string
