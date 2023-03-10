from PySide6 import QtWidgets
from bookkeeper.view.interface import MainWindow


class BudgetTable(QtWidgets.QTableWidget):
    def __init__(self, main_window: 'MainWindow'):
        super(BudgetTable, self).__init__()
        self.main_window = main_window
        self.expense_calculator = ExpenseCalculator(self.main_window.expenses_data)
        self.setRowCount(3)
        self.setColumnCount(2)
        header = self.horizontalHeader()
        self.setHorizontalHeaderLabels("Расход Бюджет".split())
        self.setVerticalHeaderLabels("День Неделя Месяц".split())
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        self.is_rendering = False
        self.cellChanged.connect(self.update_budget)

    def update_budget(self, row, column):
        if self.is_rendering:
            return
        budget = self.main_window.budget_data[row]
        item = self.item(row, column).text()

        if column == 1:
            budget.amount = int(item)

        self.main_window.db.budget.update(budget)

    def set_data(self):
        self.is_rendering = True
        for i, row in enumerate(self.main_window.budget_data):
            amount = row.amount
            expense = self.expense_calculator.calculate(row.type)
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(str(amount)))
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(str(expense)))
        self.is_rendering = False

    def update_table(self):
        self.clearContents()
        self.set_data()

