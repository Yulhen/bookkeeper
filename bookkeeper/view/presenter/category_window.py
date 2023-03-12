from typing import cast

from bookkeeper.models.category import Category
from bookkeeper.view.models import ObjectManager
from bookkeeper.view.presenter.base import PresenterBase
from bookkeeper.view.widgets.category_window import CorrectionCategoryWindowView


class CorrectionCategoryWindowPresenter(PresenterBase):
    def __init__(self, view: CorrectionCategoryWindowView, db: ObjectManager):
        super().__init__(view, db)

        self.categories: list[Category] = self.db.category.get_all()
        self.categories_dict = {cat.name: cat for cat in self.categories}

    @property
    def view(self) -> CorrectionCategoryWindowView:
        return cast(CorrectionCategoryWindowView, self._view)

    def set_data(self) -> None:
        self.view.set_layout(
            categories=list(self.categories_dict.keys()), handler=self.open_main_window
        )

    def get_categories_names(self) -> list[str]:
        return [cat.name for cat in self.categories]

    def update_view(self) -> None:
        self.categories = list(self.categories_dict.values())
        self.view.categories_field.clear()
        self.view.categories_field.insert(" ".join(self.get_categories_names()))
        self.set_data()

    def open_main_window(self):
        cats = self.view.categories_field.text().split()

        deleted_cats = set(self.categories_dict.keys()) - set(cats)
        added_cats = set(cats) - set(self.categories_dict.keys())

        for cat_name in added_cats:
            obj = Category(name=cat_name)
            obj.pk = self.db.category.add(obj)
            self.categories_dict[cat_name] = obj

        for cat_name in deleted_cats:
            obj = self.categories_dict[cat_name]
            self.db.category.delete(obj.pk)
            del self.categories_dict[cat_name]

        self.update_view()
        self.view.hide()

    def get_category(self, pk: int) -> Category | None:
        for cat in self.categories:
            if cat.pk == pk:
                return cat
        return None

    def open_window(self) -> None:
        self.set_data()
        self.view.show()
