from __future__ import annotations
from ._integration import OdooIntegration


class PaymentTermModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_payment_term_id_by_name(self, payment_term_name: str) -> int:
        response = self.search(
            "account.payment.term", [[["name", "=", payment_term_name]]]
        )
        if response:
            return response[0]
        raise Exception(f"Payment term name '{payment_term_name}' not found")
