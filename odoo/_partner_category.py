from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class PartnerCategoryModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_category_by_id(self, category_id: int) -> dict[str, Any]:
        response = self.read("res.partner.category", [category_id])
        if response:
            return response[0]
        raise Exception(f"Category '{category_id}' not found")

    def get_category_id_by_name(self, category_name: str) -> int:
        response = self.search("res.partner.category", [[["name", "=", category_name]]])
        if response:
            return response[0]
        raise Exception(f"Category '{category_name}' not found")
