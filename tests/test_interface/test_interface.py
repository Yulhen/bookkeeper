import sqlite3

from bookkeeper.view.interface import MainWindow

from pytestqt.qt_compat import qt_api

import pytest


@pytest.fixture
def db_file():
    db_file = "static/test_tmp.db"

    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        c.execute(
            """
            CREATE TABLE budget (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                amount int NOT NULL, 
                type text, 
                added_date datetime
            )
        """
        )
        c.execute(
            """
            CREATE TABLE category (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                parent INT NULL,
                name TEXT NOT NULL
            )
        """
        )
        c.execute(
            """
            CREATE TABLE expense (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                amount int NOT NULL,
                category int NOT NULL,
                comment TEXT NOT NULL,
                added_date datetime NOT NULL, expense_date datetime NOT NULL,
                FOREIGN KEY(category) REFERENCES category(pk)
            )
        """
        )
        con.commit()

    yield db_file

    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        c.execute(f"drop table budget")
        c.execute(f"drop table expense")
        c.execute(f"drop table category")
        con.commit()


@pytest.fixture
def app_mock(db_file):
    class MainWindowMock(MainWindow):
        DB_FILE = db_file

    return MainWindowMock()


def test_create_category(qtbot, app_mock, db_file):
    qtbot.addWidget(app_mock)

    assert app_mock.category_view.categories_field.text() == ""

    qtbot.mouseClick(app_mock.edit_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    categories = ["Category1", "Category2"]
    app_mock.category_view.categories_field.setText(" ".join(categories))

    qtbot.mouseClick(
        app_mock.category_presenter.view.save_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton,
    )
    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        db_categories = c.execute("SELECT * FROM category").fetchall()

    assert len(db_categories) == len(categories)
