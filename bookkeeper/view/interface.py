import sys

from PySide6 import QtWidgets, QtGui, QtCore


class ExpensesTable(QtWidgets.QTableWidget):
    def __init__(self):
        super(ExpensesTable, self).__init__()
        self.setRowCount(20)
        self.setColumnCount(4)
        header = self.horizontalHeader()
        self.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()

    def set_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(x.capitalize()))


class BudgetTable(QtWidgets.QTableWidget):
    def __init__(self):
        super(BudgetTable, self).__init__()
        self.setRowCount(3)
        self.setColumnCount(2)
        header = self.horizontalHeader()
        self.setHorizontalHeaderLabels("Расход Бюджет".split())
        self.setVerticalHeaderLabels("День Неделя Месяц".split())
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


class CorrectionCategoryWindow(QtWidgets.QMainWindow):
    def __init__(self, main_window: "MainWindow"):
        super(CorrectionCategoryWindow, self).__init__()
        self.setWindowTitle("Редактор списка категорий")

        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()
        self.layout.addWidget(
            QtWidgets.QLabel(
                "Для изменения списка категорий покупок запишите новый список, разделяя категории пробелом."
            )
        )

        self.categories_field = QtWidgets.QLineEdit(
            " ".join(self.main_window.categories)
        )
        self.layout.addWidget(self.categories_field)

        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.save_button.move(275, 200)
        self.save_button.clicked.connect(self.open_main_window)

        self.layout.addWidget(self.save_button)

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def open_main_window(self):
        self.main_window.update_categories(
            categories=self.categories_field.text().split()
        )
        self.hide()
        self.main_window.show()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Финансовый помощник")
        self.layout = QtWidgets.QVBoxLayout()

        widget = QtWidgets.QWidget()
        self.layout.addWidget(
            QtWidgets.QLabel("Здравствуйте! Ниже представлены Ваши последние расходы")
        )

        self.expenses_table = ExpensesTable()
        self.expenses_data = [
            ["2023-02-19", "300", "Одежда", "Магазин на диване"],
            ["2023-02-19", "0", "Еда", "Овсянка от Лизы"],
        ]
        self.expenses_table.set_data(self.expenses_data)
        self.layout.addWidget(self.expenses_table)

        self.budget_table = BudgetTable()
        self.layout.addWidget(
            QtWidgets.QLabel("Ваши расходы за выбранный период и бюджет")
        )
        self.layout.addWidget(self.budget_table)

        self.categories: list[str] = ["Еда", "Одежда", "Услуги"]

        expense_form = QtWidgets.QWidget(self)
        form_layout = QtWidgets.QFormLayout()
        expense_form.setLayout(form_layout)
        self.sum_field = QtWidgets.QLineEdit(expense_form)
        form_layout.addRow("Сумма", self.sum_field)
        form_layout.addRow("Категория", self.create_category_menu(expense_form))

        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setToolTip("Нажмите, чтобы добавить запись в таблицу расходов")

        self.layout.addWidget(expense_form)
        self.layout.addWidget(self.add_button)

        widget.update()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def create_category_menu(
        self, parent_form: QtWidgets.QWidget
    ) -> QtWidgets.QHBoxLayout:
        box = QtWidgets.QHBoxLayout()

        self.category_field = QtWidgets.QComboBox(parent_form)
        self.category_field.insertItems(0, self.get_categories())

        edit_button = QtWidgets.QPushButton("Редактировать", self)
        edit_button.clicked.connect(self.open_form_window)
        edit_button.setToolTip("Нажмите для изменения списка категорий")

        box.addWidget(self.category_field)
        box.addWidget(edit_button)

        return box

    def get_categories(self) -> list[str]:
        return list(set(self.categories))

    def update_categories(self, categories: list[str]) -> None:
        self.categories = categories
        self.category_field.clear()
        self.category_field.insertItems(0, self.get_categories())

    def open_form_window(self):
        self.form_window = CorrectionCategoryWindow(self)
        self.form_window.show()
        self.hide()


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
