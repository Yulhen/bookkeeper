from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


class RepositoryFactory:

    @staticmethod
    def get_repository(cls: type, **kwargs) -> AbstractRepository:
        return SQLiteRepository(cls=cls, db_file=kwargs.get('db_file'))


class ObjectManager:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def category(self) -> AbstractRepository:
        return RepositoryFactory.get_repository(cls=Category, **self.kwargs)

    @property
    def expense(self) -> AbstractRepository:
        return RepositoryFactory.get_repository(cls=Expense, **self.kwargs)

    @property
    def budget(self) -> AbstractRepository:
        return RepositoryFactory.get_repository(cls=Budget, **self.kwargs)
