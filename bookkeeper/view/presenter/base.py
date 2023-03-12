import abc

from bookkeeper.view.models import ObjectManager
from bookkeeper.view.widgets.base_view import ViewBase


class PresenterBase(abc.ABC):
    def __init__(self, view: ViewBase, db: ObjectManager):
        self._view = view
        self._db = db

    @property
    def db(self) -> ObjectManager:
        return self._db

    @property
    @abc.abstractmethod
    def view(self) -> ViewBase:
        raise NotImplementedError

    @abc.abstractmethod
    def set_data(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update_view(self) -> None:
        raise NotImplementedError
