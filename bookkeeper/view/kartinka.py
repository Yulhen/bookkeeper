import sys
from PySide6 import QtWidgets, QtGui, QtCore


app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QMainWindow()
window.setWindowTitle("Мои финансы")
window.resize(600, 400)

central_widget = QtWidgets.QWidget()
window.setCentralWidget(central_widget)

vertical_layout = QtWidgets.QVBoxLayout()
vertical_layout.addWidget(
    QtWidgets.QLabel("Здравствуйте! Вас приветствует финансовый помощник.")
)

text = QtWidgets.QLabel("<b>Ваши расходы</b>")
vertical_layout.addWidget(text)

expenses_table = QtWidgets.QTableWidget(4, 20)
expenses_table.setColumnCount(4)
expenses_table.setRowCount(20)
expenses_table.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())
header = expenses_table.horizontalHeader()
header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

expenses_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
expenses_table.verticalHeader().hide()

vertical_layout.addWidget(expenses_table)


def set_data(data: list[list[str]]):
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            expenses_table.setItem(i, j, QtWidgets.QTableWidgetItem(x.capitalize()))


datas = [["10-04-2021", "100", "hurma", "eda"], ["11-09-2022", "300", "soska", "lolka"]]
set_data(datas)

vertical_layout.addWidget(QtWidgets.QLabel("<b>Ваш бюджет</b>"))
budget_table = QtWidgets.QTableWidget(3, 4)
budget_table.setColumnCount(2)
budget_table.setRowCount(3)
budget_table.setHorizontalHeaderLabels("Сумма Бюджет".split())
budget_table.setVerticalHeaderLabels("День Неделя Месяц".split())
header = budget_table.horizontalHeader()
header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)


budget_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
vertical_layout.addWidget(budget_table)

hl = QtWidgets.QHBoxLayout()
hl.addWidget(QtWidgets.QLabel("Сумма"))
hl.addWidget(QtWidgets.QLineEdit("0"))
vertical_layout.addLayout(hl)


combo_box = QtWidgets.QComboBox()
categories = ["Еда", "Канцелярия", "Одежда и обувь", "Бытовая химия", "Услуги"]
combo_box.insertItems(0, categories)

hl2 = QtWidgets.QHBoxLayout()
hl2.addWidget(QtWidgets.QLabel("Категория"))
hl2.addWidget(combo_box)

correct_category_btn = QtWidgets.QPushButton("Редактировать")
correct_window = QtWidgets.QMdiSubWindow
correct_category_btn.clicked.connect(correct_window)

hl2.addWidget(correct_category_btn)
vertical_layout.addLayout(hl2)

# btn = QtWidgets.QPushButton("Спасибо! До свидания!")
# btn.clicked.connect(app.quit)
# vertical_layout.addWidget(btn)

central_widget.setLayout(vertical_layout)
central_widget.setToolTip("Да, вот сюда")

window.show()
sys.exit(app.exec())
