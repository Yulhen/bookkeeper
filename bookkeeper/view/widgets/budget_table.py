from PySide6 import QtWidgets

from bookkeeper.view.widgets.base_view import ViewBase


class BudgetTableView(QtWidgets.QTableWidget, ViewBase):
    HORIZONTAL_HEADER_LABELS = ["Расход", "Бюджет"]
    VERTICAL_HEADER_LABELS = ["День", "Неделя", "Месяц"]

    def __init__(self):
        super().__init__()
        self.setRowCount(3)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.HORIZONTAL_HEADER_LABELS)
        self.setVerticalHeaderLabels(self.VERTICAL_HEADER_LABELS)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
