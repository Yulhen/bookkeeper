from PySide6 import QtWidgets

from bookkeeper.view.widgets.base_view import ViewBase


class CorrectionCategoryWindowView(QtWidgets.QMainWindow, ViewBase):
    TITLE = "Редактор списка категорий"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.TITLE)

    def set_layout(self, categories: list[str], handler) -> None:
        self.layout = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()
        self.layout.addWidget(
            QtWidgets.QLabel(
                "Для изменения списка категорий покупок запишите новый список, разделяя категории пробелом."
            )
        )

        self.categories_field = QtWidgets.QLineEdit(" ".join(categories))
        self.layout.addWidget(self.categories_field)

        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.save_button.move(275, 200)
        self.save_button.clicked.connect(handler)

        self.layout.addWidget(self.save_button)

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
