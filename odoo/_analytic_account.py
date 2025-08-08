from __future__ import annotations
from ._integration import OdooIntegration


class AnalyticAccountModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_analytic_account_id_by_name(self, analytic_account_name: str) -> int:
        response = self.search(
            "account.analytic.account", [[["name", "=", analytic_account_name]]]
        )
        if response:
            return response[0]
        raise Exception(f"Analytic account name '{analytic_account_name}' not found")
