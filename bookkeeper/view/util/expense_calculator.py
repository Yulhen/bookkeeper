from datetime import datetime, timedelta

from bookkeeper.models.budget import BudgetType
from bookkeeper.models.expense import Expense


class ExpenseCalculator:
    def __init__(self, expenses_data: list[Expense]):
        self.data = expenses_data

    def calculate(self, b_type: BudgetType, dt: datetime | None = None) -> float:
        dt = dt or datetime.now()
        offset = {
            BudgetType.DAILY: timedelta(days=1),
            BudgetType.WEEKLY: timedelta(days=7),
            BudgetType.MONTHLY: timedelta(days=30),
        }[b_type]
        return sum(e.amount for e in self.data if dt - offset <= e.added_date <= dt)
