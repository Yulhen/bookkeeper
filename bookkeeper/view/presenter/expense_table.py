from datetime import datetime
from typing import cast, TYPE_CHECKING

from PySide6 import QtWidgets

from bookkeeper.models.expense import Expense
from bookkeeper.view.models import ObjectManager
from bookkeeper.view.presenter.base import PresenterBase
from bookkeeper.view.widgets.base_view import ViewBase
from bookkeeper.view.widgets.expense_table import ExpensesTableView

if TYPE_CHECKING:
    from bookkeeper.view.interface import MainWindow


class ExpensesTablePresenter(PresenterBase):
    DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"
    COLUMNS = ["added_date", "amount", "category", "comment"]

    def __init__(self, view: ViewBase, db: ObjectManager, main_window: "MainWindow"):
        super().__init__(view, db)

        self.main_window = main_window

        self.expenses_data: list[Expense] = self.db.expense.get_all()
        self.is_rendering = False

        self.expense_form = QtWidgets.QWidget(main_window)
        form_layout = QtWidgets.QFormLayout()

        self.expense_form.setLayout(form_layout)
        self.sum_field = QtWidgets.QLineEdit(self.expense_form)
        form_layout.addRow("Сумма", self.sum_field)
        form_layout.addRow(
            "Категория", main_window.create_category_menu(self.expense_form)
        )

        self.add_button = QtWidgets.QPushButton("Добавить", main_window)
        self.add_button.setToolTip("Нажмите, чтобы добавить запись в таблицу расходов")
        self.add_button.clicked.connect(self.add_new_row)

        self.view.cellChanged.connect(self.update_expense)

    @property
    def view(self) -> ExpensesTableView:
        return cast(ExpensesTableView, self._view)

    def update_expense(self, row, column):
        if self.is_rendering:
            return
        expense = self.expenses_data[row]
        item = self.view.item(row, column).text()

        if column == 0:
            expense.added_date = datetime.strptime(item, self.DATE_FORMAT)
        if column == 1:
            expense.amount = int(item)
        elif column == 3:
            expense.comment = item

        self.db.expense.update(expense)
        self.main_window.budget_presenter.update_view()

    def update_view(self):
        self.view.clearContents()
        row_count = max(5, len(self.expenses_data))
        self.view.setRowCount(row_count)
        self.set_data()

    def set_data(self):
        self.is_rendering = True
        for i, row in enumerate(self.expenses_data):
            for j, col in enumerate(self.COLUMNS):
                item = getattr(row, col)
                if isinstance(item, datetime):
                    item = item.strftime(self.DATE_FORMAT)
                elif col == "category":
                    cat = self.main_window.category_presenter.get_category(pk=item)
                    item = cat.name
                else:
                    item = str(item)
                self.view.setItem(i, j, QtWidgets.QTableWidgetItem(item))
        self.is_rendering = False

    def add_new_row(self):
        cat_name = self.main_window.category_field.currentText()
        obj = Expense(
            added_date=datetime.now(),
            expense_date=datetime.now(),
            amount=int(self.sum_field.text()),
            category=self.main_window.category_presenter.categories_dict[cat_name].pk,
            comment=" ",
        )
        obj.pk = self.db.expense.add(obj)
        self.expenses_data.append(obj)

        self.update_view()
        self.main_window.budget_presenter.update_view()
