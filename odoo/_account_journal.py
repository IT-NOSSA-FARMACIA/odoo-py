from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class AccountJournalModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_journal_id_by_name(
        self, journal_name: str, company_id: int | None = None
    ) -> int:
        if company_id:
            response = self.search(
                "account.journal",
                [[["name", "=", journal_name], ["company_id", "=", company_id]]],
            )
        else:
            response = self.search("account.journal", [[["name", "=", journal_name]]])
        if response:
            return response[0]
        raise Exception(f"Journal '{journal_name}' not found")

    def get_journal_by_id(
        self, journal_id: int, fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        response = self.read("account.journal", [journal_id], fields)
        return response
