"""
Модель категории расходов
"""
from enum import Enum
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterator

from ..repository.abstract_repository import AbstractRepository


class BudgetType(str, Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

@dataclass
class Budget:
    pk: int
    amount: int
    type: BudgetType
    added_date: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_dict(cls, data: dict) -> 'Budget':
        return cls(
            amount=data['amount'],
            pk=data['pk'],
            added_date=datetime.fromisoformat(data['added_date']),
            type=BudgetType(data['type'])
        )


'''CREATE TABLE budget (
	pk int PRIMARY KEY,
	amount int NOT NULL
)'''