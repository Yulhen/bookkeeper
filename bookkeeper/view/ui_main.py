# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(884, 600)
        MainWindow.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(194, 129, 194, 255), stop:1 rgba(242, 197, 197, 255));\n"
            'font: 9pt "Verdana";'
        )
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(41, 31, 421, 522))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_expense = QLabel(self.widget)
        self.label_expense.setObjectName("label_expense")
        self.label_expense.setStyleSheet("background-color:rgb(197, 133, 194);\n" "")

        self.verticalLayout.addWidget(self.label_expense)

        self.table_expense = QTableWidget(self.widget)
        if self.table_expense.columnCount() < 4:
            self.table_expense.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_expense.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_expense.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_expense.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_expense.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if self.table_expense.rowCount() < 20:
            self.table_expense.setRowCount(20)
        self.table_expense.setObjectName("table_expense")
        self.table_expense.setStyleSheet(
            "border-color: rgb(255, 0, 255);\n"
            "alternate-background-color: rgb(255, 170, 255);"
        )
        self.table_expense.setRowCount(20)
        self.table_expense.setColumnCount(4)
        self.table_expense.horizontalHeader().setStretchLastSection(True)
        self.table_expense.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.table_expense)

        self.label_budget = QLabel(self.widget)
        self.label_budget.setObjectName("label_budget")
        self.label_budget.setStyleSheet(
            "background-color:rgb(212, 170, 175);\n" "\n" "\n" ""
        )

        self.verticalLayout.addWidget(self.label_budget)

        self.tablebudget = QTableWidget(self.widget)
        if self.tablebudget.columnCount() < 2:
            self.tablebudget.setColumnCount(2)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablebudget.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tablebudget.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        if self.tablebudget.rowCount() < 3:
            self.tablebudget.setRowCount(3)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tablebudget.setVerticalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tablebudget.setVerticalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tablebudget.setVerticalHeaderItem(2, __qtablewidgetitem8)
        self.tablebudget.setObjectName("tablebudget")
        self.tablebudget.setRowCount(3)
        self.tablebudget.setColumnCount(2)
        self.tablebudget.horizontalHeader().setCascadingSectionResizes(False)
        self.tablebudget.horizontalHeader().setStretchLastSection(True)
        self.tablebudget.verticalHeader().setCascadingSectionResizes(False)
        self.tablebudget.verticalHeader().setDefaultSectionSize(50)
        self.tablebudget.verticalHeader().setProperty("showSortIndicator", False)
        self.tablebudget.verticalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tablebudget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sum_label = QLabel(self.widget)
        self.sum_label.setObjectName("sum_label")
        self.sum_label.setStyleSheet("background-color: rgb(215, 159, 195);")

        self.horizontalLayout.addWidget(self.sum_label)

        self.sum_edit_line = QLineEdit(self.widget)
        self.sum_edit_line.setObjectName("sum_edit_line")
        self.sum_edit_line.setStyleSheet("background-color: rgb(252, 204, 208);")

        self.horizontalLayout.addWidget(self.sum_edit_line)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.category_label = QLabel(self.widget)
        self.category_label.setObjectName("category_label")
        self.category_label.setStyleSheet("background-color: rgb(215, 159, 195);")

        self.horizontalLayout_2.addWidget(self.category_label)

        self.categories_box = QComboBox(self.widget)
        self.categories_box.addItem("")
        self.categories_box.addItem("")
        self.categories_box.addItem("")
        self.categories_box.setObjectName("categories_box")

        self.horizontalLayout_2.addWidget(self.categories_box)

        self.correct_category_btn = QPushButton(self.widget)
        self.correct_category_btn.setObjectName("correct_category_btn")

        self.horizontalLayout_2.addWidget(self.correct_category_btn)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.add_expense = QPushButton(self.widget)
        self.add_expense.setObjectName("add_expense")

        self.verticalLayout.addWidget(self.add_expense)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow",
                "\u0424\u0438\u043d\u0430\u043d\u0441\u043e\u0432\u044b\u0439 \u043f\u043e\u043c\u043e\u0449\u043d\u0438\u043a",
                None,
            )
        )
        self.label_expense.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0420\u0430\u0441\u0445\u043e\u0434\u044b", None
            )
        )
        ___qtablewidgetitem = self.table_expense.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("MainWindow", "\u0414\u0430\u0442\u0430", None)
        )
        ___qtablewidgetitem1 = self.table_expense.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0421\u0443\u043c\u043c\u0430", None
            )
        )
        ___qtablewidgetitem2 = self.table_expense.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f",
                None,
            )
        )
        ___qtablewidgetitem3 = self.table_expense.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439",
                None,
            )
        )
        self.label_budget.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0411\u044e\u0434\u0436\u0435\u0442", None
            )
        )
        ___qtablewidgetitem4 = self.tablebudget.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0420\u0430\u0441\u0445\u043e\u0434\u044b", None
            )
        )
        ___qtablewidgetitem5 = self.tablebudget.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0411\u044e\u0434\u0436\u0435\u0442", None
            )
        )
        ___qtablewidgetitem6 = self.tablebudget.verticalHeaderItem(0)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate("MainWindow", "\u0414\u0435\u043d\u044c", None)
        )
        ___qtablewidgetitem7 = self.tablebudget.verticalHeaderItem(1)
        ___qtablewidgetitem7.setText(
            QCoreApplication.translate(
                "MainWindow", "\u041d\u0435\u0434\u0435\u043b\u044f", None
            )
        )
        ___qtablewidgetitem8 = self.tablebudget.verticalHeaderItem(2)
        ___qtablewidgetitem8.setText(
            QCoreApplication.translate(
                "MainWindow", "\u041c\u0435\u0441\u044f\u0446", None
            )
        )
        self.sum_label.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0421\u0443\u043c\u043c\u0430", None
            )
        )
        self.sum_edit_line.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "0", None)
        )
        self.category_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f",
                None,
            )
        )
        self.categories_box.setItemText(
            0, QCoreApplication.translate("MainWindow", "\u0415\u0434\u0430", None)
        )
        self.categories_box.setItemText(
            1,
            QCoreApplication.translate(
                "MainWindow", "\u0423\u0441\u043b\u0443\u0433\u0438", None
            ),
        )
        self.categories_box.setItemText(
            2,
            QCoreApplication.translate(
                "MainWindow", "\u041e\u0434\u0435\u0436\u0434\u0430", None
            ),
        )

        self.correct_category_btn.setText(
            QCoreApplication.translate(
                "MainWindow",
                "\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c",
                None,
            )
        )
        self.add_expense.setText(
            QCoreApplication.translate(
                "MainWindow", "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None
            )
        )

    # retranslateUi
