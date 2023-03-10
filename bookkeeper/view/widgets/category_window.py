from PySide6 import QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.view.interface import MainWindow


class CorrectionCategoryWindow(QtWidgets.QMainWindow):
    def __init__(self, main_window: MainWindow):
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
            " ".join(self.main_window.categories_dict.keys())
        )
        self.layout.addWidget(self.categories_field)

        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.save_button.move(275, 200)
        self.save_button.clicked.connect(self.open_main_window)

        self.layout.addWidget(self.save_button)

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def open_main_window(self):
        cats = self.categories_field.text().split()

        deleted_cats = set(self.main_window.categories_dict.keys()) - set(cats)
        added_cats = set(cats) - set(self.main_window.categories_dict.keys())

        for cat_name in added_cats:
            obj = Category(name=cat_name)
            obj.pk = self.main_window.db.category.add(obj)
            self.main_window.categories_dict[cat_name] = obj

        for cat_name in deleted_cats:
            obj = self.main_window.categories_dict[cat_name]
            self.main_window.db.category.delete(obj.pk)
            del self.main_window.categories_dict[cat_name]

        self.main_window.update_categories(
            categories=list(self.main_window.categories_dict.values())
        )
        self.hide()