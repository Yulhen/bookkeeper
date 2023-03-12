import sys

from PySide6 import QtWidgets

from bookkeeper.view.models import ObjectManager
from bookkeeper.view.presenter.budget_table import BudgetTablePresenter
from bookkeeper.view.presenter.category_window import CorrectionCategoryWindowPresenter
from bookkeeper.view.presenter.expense_table import ExpensesTablePresenter
from bookkeeper.view.widgets.budget_table import BudgetTableView
from bookkeeper.view.widgets.category_window import CorrectionCategoryWindowView
from bookkeeper.view.widgets.expense_table import ExpensesTableView


STYLESHEET = """
    QMainWindow {
        background-image: url("static/koteki.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""


class MainWindow(QtWidgets.QMainWindow):
    WINDOW_TITLE = "Финансовый помощник"
    DB_FILE = "static/bookkeeper.db"

    def __init__(self):
        super().__init__()

        self.db = ObjectManager(db_file=self.DB_FILE)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.layout = QtWidgets.QVBoxLayout()

        widget = QtWidgets.QWidget()
        self.layout.addWidget(
            QtWidgets.QLabel("Здравствуйте! Ниже представлены Ваши последние расходы")
        )

        self.category_view = CorrectionCategoryWindowView()
        self.category_presenter = CorrectionCategoryWindowPresenter(
            self.category_view, self.db
        )
        self.category_presenter.set_data()

        self.expenses_table = ExpensesTableView()
        self.layout.addWidget(self.expenses_table)

        self.expenses_presenter = ExpensesTablePresenter(
            self.expenses_table, self.db, self
        )
        self.expenses_presenter.update_view()

        self.budget_table = BudgetTableView()
        self.layout.addWidget(self.budget_table)

        self.budget_presenter = BudgetTablePresenter(self.budget_table, self.db)
        self.budget_presenter.set_data()

        self.layout.addWidget(
            QtWidgets.QLabel("Ваши расходы за выбранный период и бюджет")
        )

        self.layout.addWidget(self.expenses_presenter.expense_form)
        self.layout.addWidget(self.expenses_presenter.add_button)

        widget.update()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)

    def create_category_menu(
        self, parent_form: QtWidgets.QWidget
    ) -> QtWidgets.QHBoxLayout:
        box = QtWidgets.QHBoxLayout()

        self.category_field = QtWidgets.QComboBox(parent_form)
        self.category_field.insertItems(
            0, self.category_presenter.get_categories_names()
        )

        self.edit_button = QtWidgets.QPushButton("Редактировать", self)
        self.edit_button.clicked.connect(self.category_presenter.open_window)
        self.edit_button.setToolTip("Нажмите для изменения списка категорий")

        box.addWidget(self.category_field)
        box.addWidget(self.edit_button)

        return box


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
