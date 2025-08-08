from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class SaleOrderModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_sale_order_by_any_filter(self, filter: list[Any]) -> list[int]:
        response = self.search("sale.order", [filter])
        return response

    def get_sale_order_by_state(self, state: list[str]) -> list[int]:
        response = self.search("sale.order", [[["state", "in", state]]])
        return response

    def get_sale_order_by_id(
        self, sale_order_id: int, fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        response = self.read("sale.order", [sale_order_id], fields)
        return response

    def get_sale_order_line_list_by_sale_order_id(
        self, sale_order_id: int
    ) -> list[int]:
        response = self.search("sale.order.line", [[["order_id", "=", sale_order_id]]])
        return response

    def get_sale_order_line_by_id(
        self, sale_order_line_id: int
    ) -> list[dict[str, Any]]:
        response = self.read("sale.order.line", [sale_order_line_id])
        return response

    def create_sale_order_line(
        self, sale_order_line_data: dict[str, Any]
    ) -> int | list[int]:
        # sale_order_line = {
        #     "order_id": sale_order_id,
        #     "product_id": product_id,
        #     "product_uom_qty": product_quantity,
        #     "price_unit": price_unit,
        #     "discount": discount,
        #     # "x_studio_many2one_field_ZK6OA": lote_id,  # id do lote
        #     # "x_studio_data_de_validade": "2024-02-21", # data de validade (se não for passado, pega a data do lote)
        # }
        # if lote_id:
        #     sale_order_line["x_studio_many2one_field_ZK6OA"] = lote_id
        response = self.create("sale.order.line", [sale_order_line_data])
        return response

    def create_sale_order(self, sale_order_data: dict[str, Any]) -> int | list[int]:
        # sale_order = {
        #     "partner_id": partner_id,
        #     "company_id": company_id,  # serão duas empresas, addo pharm e addo pharm distribuição
        #     "warehouse_id": warehouse_id,  # warehouse de distribuiçãos (armazem)
        #     "analytic_account_id": analytic_account_id,
        # }
        response = self.create("sale.order", [sale_order_data])
        return response

    def confirm_sale_order(self, sale_order_id: int) -> dict[str, Any]:
        response = self.execute_action("sale.order", "action_confirm", sale_order_id)
        return response

    def certify_sale_order(self, sale_order_id: int) -> dict[str, Any]:
        response = self.execute_action("sale.order", "certify", sale_order_id)
        return response

    def create_invoice_from_sale_order(self, sale_order_id: int) -> dict[str, Any]:
        # sale_order_id is used as active_id (context)
        extra_context = {
            "active_id": sale_order_id,
            "active_ids": [sale_order_id],
            "active_model": "sale.order",
        }
        response = self.execute_action(
            "sale.advance.payment.inv", "create", [], extra_context
        )
        return response

    def confirm_invoice_from_sale_order(
        self, invoice_id: int, sale_order_id: int
    ) -> dict[str, Any]:
        # sale_order_id is used as active_id (context)
        extra_context = {
            "active_id": sale_order_id,
            "active_ids": [sale_order_id],
            "active_model": "sale.order",
        }
        response = self.execute_action(
            "sale.advance.payment.inv", "create_invoices", invoice_id, extra_context
        )
        return response

    def certify_invoice_from_sale_order(self, sale_order_id: int) -> dict[str, Any]:
        response = self.execute_action("sale.order", "certify", sale_order_id)
        return response

    def get_sale_order_message(self, message_id: int) -> list[dict[str, Any]]:
        response = self.read("mail.message", [message_id])
        return response

    def get_sale_order_attachment(self, attachment_id: int) -> dict[str, Any]:
        response = self.read("ir.attachment", [attachment_id])
        return response[0]

    def confirm_invoice_by_button_action_by_invoice_id(
        self, invoice_id: int
    ) -> dict[str, Any]:
        response = self.execute_action("account.move", "action_post", invoice_id)
        return response

    def get_invoice_id_from_sale_order(self, sale_order_id: int) -> int:
        response = self.execute_action(
            "sale.order", "action_view_invoice", sale_order_id
        )
        return response["res_id"]

    def invoice_force_creation(self, invoice_id: int) -> bool:
        response = self.update("account.move", invoice_id, {"force_open": True})
        return response

    def invoice_insert_footer_notes(self, invoice_id: int, notes: str) -> bool:
        response = self.update("account.move", invoice_id, {"footer_notes": notes})
        return response

    # def invoice_insert_narration(self, invoice_id, narration):
    #     response = self.update("account.move", invoice_id, {"narration": narration})
    #     return response

    # def get_invoice(self, invoice_id):
    #     response = self.read("account.move", [invoice_id])
    #     return response[0]
