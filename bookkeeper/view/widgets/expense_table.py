from PySide6 import QtWidgets
from bookkeeper.view.interface import MainWindow


class ExpensesTable(QtWidgets.QTableWidget):
    DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"

    def __init__(self, main_window: 'MainWindow'):
        super(ExpensesTable, self).__init__()
        self.main_window = main_window
        row_count = max(5, len(self.main_window.expenses_data))
        self.setRowCount(row_count)
        self.setColumnCount(4)
        header = self.horizontalHeader()
        self.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())
        self.columns = ['added_date', 'amount', 'category', 'comment']
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.verticalHeader().hide()

        self.is_rendering = False
        self.cellChanged.connect(self.update_expense)

    def update_expense(self, row, column):
        if self.is_rendering:
            return
        expense = self.main_window.expenses_data[row]
        item = self.item(row, column).text()

        if column == 0:
            expense.added_date = datetime.strptime(item, self.DATE_FORMAT)
        if column == 1:
            expense.amount = int(item)
        elif column == 3:
            expense.comment = item

        self.main_window.db.expense.update(expense)

    def update_table(self):
        self.clearContents()
        self.set_data()

    def set_data(self):
        self.is_rendering = True
        for i, row in enumerate(self.main_window.expenses_data):
            for j, col in enumerate(self.columns):
                item = getattr(row, col)
                if isinstance(item, datetime):
                    item = item.strftime(self.DATE_FORMAT)
                elif col == 'category':
                    cat = self.main_window.get_category(pk=item)
                    item = cat.name
                else:
                    item = str(item)
                self.setItem(i, j, QtWidgets.QTableWidgetItem(item))
        self.is_rendering = False

