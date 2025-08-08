from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class AccountTaxModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_tax_id_by_name(self, tax_name: str, company_id: int | None = None) -> int:
        if company_id:
            response = self.search(
                "account.tax",
                [[["name", "=", tax_name], ["company_id", "=", company_id]]],
            )
        else:
            response = self.search("account.tax", [[["name", "=", tax_name]]])
        if response:
            return response[0]
        raise Exception(f"Tax '{tax_name}' not found")

    def get_tax_by_id(
        self, tax_id: int, fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        response = self.read("account.tax", [tax_id], fields)
        return response
