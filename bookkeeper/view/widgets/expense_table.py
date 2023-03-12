from PySide6 import QtWidgets

from bookkeeper.view.widgets.base_view import ViewBase


class ExpensesTableView(QtWidgets.QTableWidget, ViewBase):
    HORIZONTAL_HEADER_LABELS = ["Дата", "Сумма", "Категория", "Комментарий"]
    DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"

    def __init__(self):
        super().__init__()
        self.setRowCount(5)
        self.setColumnCount(4)
        header = self.horizontalHeader()
        self.setHorizontalHeaderLabels(self.HORIZONTAL_HEADER_LABELS)

        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.verticalHeader().hide()
