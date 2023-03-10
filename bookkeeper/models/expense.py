"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        return cls(
            amount=data['amount'],
            category=data['category'],
            comment=data['comment'],
            pk=data['pk'],
            expense_date=datetime.fromisoformat(data['expense_date']),
            added_date=datetime.fromisoformat(data['added_date'])
        )
