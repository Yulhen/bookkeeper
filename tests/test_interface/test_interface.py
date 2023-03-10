# from bookkeeper.repository.memory_repository import MemoryRepository
# from bookkeeper.view.interface import MainWindow
# from pytestqt.qt_compat import qt_api
#
# import pytest
#
#
# @pytest.fixture
# def custom_class():
#     class Custom():
#         pk = 0
#
#     return Custom
#
#
# def test_hello(qtbot):
#     widget = MainWindow()
#     qtbot.addWidget(widget)
#     qtbot.mouseClick(widget.sum_field)
#     widget.sum_field.
#     qtbot.
#     # qtbot.mouseClick(widget.expense_form, qt_api.QtCore.Qt.MouseButton.LeftButton)
#     assert widget.greet_label.text() == "Hello!"
#
#
# @pytest.fixture
# def repo():
#     return None
#     # return MemoryRepository()
#
from bookkeeper.view.interface import MainWindow


def test_interface():
    MainWindow()
    assert True
