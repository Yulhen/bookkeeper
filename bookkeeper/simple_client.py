"""
Простой тестовый скрипт для терминала
"""
import sqlite3

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

db_name = ':memory:'
cat_repo = SQLiteRepository(db_file=db_name, cls=Category)
exp_repo = SQLiteRepository(db_file=db_name, cls=Expense)

with sqlite3.connect(db_name) as conn:
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE category(pk INTEGER PRIMARY KEY, name TEXT NOT NULL, parent INTEGER)')
    cur.execute(f'''
    CREATE TABLE expense(
        pk INTEGER PRIMARY KEY, 
        amount INTEGER NOT NULL, 
        category INTEGER NOT NULL,
        expense_date DATETIME NOT NULL,
        added_date DATETIME NOT NULL,
        comment TEXT NOT NULL
    )''')
    conn.commit()

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
