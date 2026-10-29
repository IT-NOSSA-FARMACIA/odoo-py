from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class AccountAccountModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_account_by_id(self, account_id: int) -> list[int]:
        response = self.read("account.account", [account_id])
        return response

    def get_account_by_any_filter(self, filter: list[Any]) -> list[int]:
        response = self.search("account.account", [filter])
        return response
