from dataclasses import dataclass

import pytest
import sqlite3

from bookkeeper.repository.sqlite_repository import SQLiteRepository


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        name: str = "name"

        @classmethod
        def from_dict(cls, data):
            return cls(**data)

    return Custom


@pytest.fixture
def repo(custom_class):
    db_file = "db_test.db"
    repo = SQLiteRepository(db_file=db_file, cls=custom_class)

    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        c.execute(
            f"create table if not exists {repo.table_name} (pk INTEGER primary key, name TEXT)"
        )
        con.commit()

    yield repo

    with sqlite3.connect(db_file) as con:
        c = con.cursor()
        c.execute(f"drop table {repo.table_name}")
        con.commit()


def test_crud(repo, custom_class):
    obj = custom_class()
    obj.pk = 0
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = None
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        o.pk = 0
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        repo.add(o)
        objects.append(o)
    assert repo.get_all({"name": "0"}) == [objects[0]]
