from typing import cast
from PySide6 import QtWidgets

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.view.models import ObjectManager
from bookkeeper.view.presenter.base import PresenterBase
from bookkeeper.view.util.expense_calculator import ExpenseCalculator
from bookkeeper.view.widgets.base_view import ViewBase


class BudgetTablePresenter(PresenterBase):
    def __init__(self, view: ViewBase, db: ObjectManager):
        super().__init__(view, db)

        self.budget_data: list[Budget] = self.db.budget.get_all()
        self.expenses_data: list[Expense] = self.db.expense.get_all()
        self.expense_calculator = ExpenseCalculator(self.expenses_data)

        self.is_rendering = False
        self.view.cellChanged.connect(self.update_budget)

    @property
    def view(self) -> QtWidgets.QTableWidget:
        return cast(QtWidgets.QTableWidget, self._view)

    def get_calculator(self) -> ExpenseCalculator:
        self.expenses_data: list[Expense] = self.db.expense.get_all()
        return ExpenseCalculator(self.expenses_data)

    def update_budget(self, row: int, column: int) -> None:
        if self.is_rendering:
            return
        budget = self.budget_data[row]
        item = self.view.item(row, column).text()

        if column == 1:
            budget.amount = int(item)

        self.db.budget.update(budget)

    def set_data(self) -> None:
        self.is_rendering = True
        for i, row in enumerate(self.budget_data):
            amount = row.amount
            calculator = self.get_calculator()
            expense = calculator.calculate(row.type)
            self.view.setItem(i, 1, QtWidgets.QTableWidgetItem(str(amount)))
            self.view.setItem(i, 0, QtWidgets.QTableWidgetItem(str(expense)))
        self.is_rendering = False

    def update_view(self) -> None:
        self.view.clearContents()
        self.set_data()
