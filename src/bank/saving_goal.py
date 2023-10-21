from tinydb import TinyDB, Query
from tinydb.operations import add


class Saving_goals:
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
        self.saving_goals: TinyDB.table_class = db.table("accounts")

    def change_balance(self, id, amount) -> None:
        self.saving_goals.update(add("current_amount", amount), Query().id == id)

    def check_saving_goal_progress(self, saving_goal_id):
        saving_goal = self.get_saving_goal(saving_goal_id)
        if not saving_goal:
            return 0

        current_balance = saving_goal.get("balance", 0)
        goal = saving_goal.get("saving_goal", 0)

        if current_balance >= goal:
            return 100  # 100% progress if the goal is achieved
        else:
            return (current_balance / goal) * 100

    def add_saving_goal(self, account: dict) -> None:
        self.saving_goals.insert(account)

    def remove_saving_goal(self, account_id: str) -> None:
        self.saving_goals.remove(Query().id == account_id)

    def get_saving_goal(self, account_id: str):
        return self.saving_goals.get(Query().id == account_id)

    def get_user_saving_goals(self, account_id: str):
        return self.saving_goals.search(Query().account_id == account_id)

    def __repr__(self):
        string = ""
        for i in self.saving_goals.all():
            string += str(i) + "\n"
        return string
