from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class CompanyModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_company_by_id(self, company_id: int) -> list[dict[str, Any]]:
        response = self.read("res.company", [company_id])
        return response

    def get_company_id_by_name(self, company_name: str) -> int:
        response = self.search("res.company", [[["name", "=", company_name]]])
        if response:
            return response[0]
        raise Exception(f"Company '{company_name}' not found")
