from datetime import datetime
from typing import Any
from inspect import get_annotations
import sqlite3
from bookkeeper.repository.abstract_repository import AbstractRepository, T


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type):
        self.db_file = db_file
        self.model: T = cls
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop("pk")

    def add(self, obj: T) -> int:
        if getattr(obj, "pk", -1) == -1 or obj.pk != 0:
            raise ValueError
        names = ", ".join(self.fields.keys())
        p = ", ".join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(
            self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        ) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(f"INSERT INTO {self.table_name}({names}) VALUES({p})", values)
            obj.pk = cur.lastrowid
            con.commit()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """Получить объект по id"""
        with sqlite3.connect(
            self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        ) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(f"SELECT * FROM {self.table_name} WHERE pk = {pk}")
            obj = cur.fetchone()
        if not obj:
            return None
        return self.model.from_dict(obj)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """Получить все записи по некоторому условию where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи"""

        with sqlite3.connect(
            self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        ) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            if where:
                condition = " and ".join(f"{col} = {val}" for col, val in where.items())
            else:
                condition = "1 = 1"
            cur.execute(f"SELECT * FROM {self.table_name} WHERE {condition}")
            objs = cur.fetchall()
        return [self.model.from_dict(obj) for obj in objs]

    @classmethod
    def _escape_update_value(cls, value: Any) -> str:
        if isinstance(value, datetime):
            return f"DATETIME('{str(value)}')"
        elif isinstance(value, str):
            return f"'{value}'"
        return str(value)

    def update(self, obj: T) -> None:
        """Обновить данные об объекте. Объект должен содержать поле pk."""
        if obj.pk is None:
            raise ValueError
        with sqlite3.connect(
            self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        ) as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            updates = ",".join(
                f"{col} = {self._escape_update_value(getattr(obj, col))}"
                for col in self.fields
            )
            cur.execute(f"UPDATE {self.table_name} SET {updates} where pk = {obj.pk} ")
            con.commit()

    def delete(self, pk: int) -> None:
        """Удалить запись"""
        with sqlite3.connect(
            self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        ) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(f"DELETE FROM {self.table_name} where pk = {pk}")
            cur.execute("SELECT changes()")
            if cur.fetchone()[0] == 0:
                raise KeyError
            con.commit()
