import sys
from datetime import datetime, timedelta
from PySide6 import QtWidgets, QtGui, QtCore

from bookkeeper.models.budget import Budget, BudgetType
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.view.models import ObjectManager


class ExpenseCalculator:

    def __init__(self, expenses_data: list[Expense]):
        self.data = expenses_data

    def calculate(self, b_type: BudgetType, dt: datetime | None = None) -> float:
        dt = dt or datetime.now()
        offset = {
            BudgetType.DAILY: timedelta(days=1),
            BudgetType.WEEKLY: timedelta(days=7),
            BudgetType.MONTHLY: timedelta(days=30)
        }[b_type]
        return sum(e.amount for e in self.data if dt - offset <= e.added_date <= dt)


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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.db = ObjectManager(db_file='bookkeeper.db')

        self.setWindowTitle("Финансовый помощник")
        self.layout = QtWidgets.QVBoxLayout()

        widget = QtWidgets.QWidget()
        self.layout.addWidget(
            QtWidgets.QLabel("Здравствуйте! Ниже представлены Ваши последние расходы")
        )

        self.budget_data: list[Budget] = self.db.budget.get_all()

        # self.categories: list[str] = ["Еда", "Одежда", "Услуги"]
        self.categories: list[Category] = self.db.category.get_all()
        self.categories_dict = {cat.name: cat for cat in self.categories}

        self.expenses_data: list[Expense] = self.db.expense.get_all()
        self.expenses_table = ExpensesTable(self)
        self.expenses_table.set_data()
        self.layout.addWidget(self.expenses_table)

        self.budget_table = BudgetTable(self)
        self.budget_table.set_data()
        self.layout.addWidget(
            QtWidgets.QLabel("Ваши расходы за выбранный период и бюджет")
        )
        self.layout.addWidget(self.budget_table)
        self.expense_form = QtWidgets.QWidget(self)
        form_layout = QtWidgets.QFormLayout()

        self.expense_form.setLayout(form_layout)
        self.sum_field = QtWidgets.QLineEdit(self.expense_form)
        form_layout.addRow("Сумма", self.sum_field)
        form_layout.addRow("Категория", self.create_category_menu(self.expense_form))

        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setToolTip("Нажмите, чтобы добавить запись в таблицу расходов")
        self.add_button.clicked.connect(self.add_new_row)

        self.layout.addWidget(self.expense_form)
        self.layout.addWidget(self.add_button)

        widget.update()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def get_category(self, pk: int) -> Category | None:
        for cat in self.categories:
            if cat.pk == pk:
                return cat
        return None

    def add_new_row(self):
        cat_name = self.category_field.currentText()
        obj = Expense(
            added_date=datetime.now(),
            expense_date=datetime.now(),
            amount=int(self.sum_field.text()),
            category=self.categories_dict[cat_name].pk,
            comment=' ',
        )
        obj.pk = self.db.expense.add(obj)
        self.expenses_data.append(obj)

        self.budget_table.update_table()
        self.expenses_table.update_table()

    def create_category_menu(
        self, parent_form: QtWidgets.QWidget
    ) -> QtWidgets.QHBoxLayout:
        box = QtWidgets.QHBoxLayout()

        self.category_field = QtWidgets.QComboBox(parent_form)
        self.category_field.insertItems(0, self.get_categories_names())

        edit_button = QtWidgets.QPushButton("Редактировать", self)
        edit_button.clicked.connect(self.open_form_window)
        edit_button.setToolTip("Нажмите для изменения списка категорий")

        box.addWidget(self.category_field)
        box.addWidget(edit_button)

        return box

    def get_categories_names(self) -> list[str]:
        return [cat.name for cat in self.categories]

    def update_categories(self, categories: list[Category]) -> None:
        self.categories = categories
        self.category_field.clear()
        self.category_field.insertItems(0, self.get_categories_names())

    def open_form_window(self):
        self.form_window = CorrectionCategoryWindow(self)
        self.form_window.show()


stylesheet = """
    QMainWindow {
        background-image: url("C:/Users/yula1/bookkeeper-master/bookkeeper-master/bookkeeper/view/koteki.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
