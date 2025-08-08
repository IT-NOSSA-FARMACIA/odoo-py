from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class PurchaseOrderModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_purchase_order_by_any_filter(self, filter: list[Any]) -> list[int]:
        response = self.search("purchase.order", [filter])
        return response

    def get_purchase_order_by_state(self, state: list[str]) -> list[int]:
        response = self.search("purchase.order", [[["state", "in", state]]])
        return response

    def get_purchase_order_by_id(
        self, purchase_order_id: int, fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        response = self.read("purchase.order", [purchase_order_id], fields)
        return response

    def get_purchase_order_line_list_by_purchase_order_id(
        self, purchase_order_id: int
    ) -> list[int]:
        response = self.search(
            "purchase.order.line", [[["order_id", "=", purchase_order_id]]]
        )
        return response

    def get_purchase_order_line_by_id(
        self, purchase_order_line_id: int
    ) -> list[dict[str, Any]]:
        response = self.read("purchase.order.line", [purchase_order_line_id])
        return response

    def create_purchase_order_line(
        self, purchase_order_line_data: dict[str, Any]
    ) -> int | list[int]:
        response = self.create("purchase.order.line", [purchase_order_line_data])
        return response

    def create_purchase_order(
        self, purchase_order_data: dict[str, Any]
    ) -> int | list[int]:
        response = self.create("purchase.order", [purchase_order_data])
        return response

    def create_invoice_from_purchase_order(
        self, purchcase_order_id: int
    ) -> dict[str, Any]:
        response = self.execute_action(
            "purchase.order", "action_create_invoice", purchcase_order_id
        )
        return response

    def confirm_invoice_purchase_order(self, invoice_id: int) -> dict[str, Any]:
        response = self.execute_action("account.move", "action_post", invoice_id)
        return response

    def invoice_insert_footer_notes(self, invoice_id: int, notes: str) -> bool:
        response = self.update("account.move", invoice_id, {"footer_notes": notes})
        return response

    """
    method: call
    method: action_post
    model_ account.move

    """

    # def confirm_purchase_order(self, purchase_order_id):
    #     response = self.execute_action("purchase.order", "action_confirm", purchase_order_id)
    #     return response

    # def certify_purchase_order(self, purchase_order_id):
    #     response = self.execute_action("purchase.order", "certify", purchase_order_id)
    #     return response
