from __future__ import annotations
from ._integration import OdooIntegration


class ProductCategoryModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_category_id_by_name(self, category_name: str) -> int:
        response = self.search("product.category", [[["name", "=", category_name]]])
        if response:
            return response[0]
        raise Exception(f"Tax '{category_name}' not found")
