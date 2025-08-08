from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class AccountInvoiceModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def invoice_send_email(self, invoice_id: int, mail_id: int) -> dict[str, Any]:
        response = self.execute_action(
            "account.invoice.send", "send_and_print_action", mail_id
        )
        return response

    def create_invoice_send_email(
        self,
        invoice_id: int,
        template_id: int,
        partner_id: int,
        partner_ids: list[int],
        attachment_id: int,
        mail_server_id: int,
        composition_mode: str,
        subject: str,
        body: str,
    ) -> dict[str, Any]:
        # onchange or call
        extra_context = {
            "active_id": invoice_id,
            "active_ids": [invoice_id],
            "active_model": "account.move",
            "custom_layout": "mail.mail_notification_paynow",
            "default_model": "account.move",
            "default_res_id": invoice_id,
            "default_res_model": "account.move",
            "default_template_id": template_id,
            "default_use_template": True,
            "force_email": True,
            "mark_invoice_as_sent": True,
            "model_description": "Fatura",
        }
        params = [
            {
                "composition_mode": composition_mode,
                "invoice_ids": [[6, False, [invoice_id]]],
                "email_from": '"Rafael Galleani" <rafegal@gmail.com>',
                "mail_server_id": mail_server_id,
                "is_print": False,
                "snailmail_is_letter": False,
                "partner_id": partner_id,
                "is_email": True,
                "partner_ids": partner_ids,
                # "partner_ids": [
                #     [
                #         6,
                #         False,
                #         [
                #             5215
                #         ]
                #     ]
                # ],
                "subject": subject,
                "body": body,
                "attachment_ids": [[6, False, [attachment_id]]],
                "template_id": template_id,
            }
        ]
        response = self.execute_action(
            "account.invoice.send", "create", params[0], extra_context=extra_context
        )
        return response

    def get_default_invoice_template(self, sale_order_id: int) -> dict[str, Any]:
        response = self.execute_action(
            "account.move", "action_invoice_sent", sale_order_id
        )
        return response

    def get_template_email(
        self, invoice_id: int, default_template_id: int
    ) -> dict[str, Any]:
        # onchange or call
        extra_context = {
            "active_id": invoice_id,
            "active_ids": [invoice_id],
            "active_model": "account.move",
            "custom_layout": "mail.mail_notification_paynow",
            "default_model": "account.move",
            "default_res_id": invoice_id,
            "default_res_model": "account.move",
            "default_template_id": default_template_id,
            "default_use_template": True,
            "force_email": True,
            "mark_invoice_as_sent": True,
            "model_description": "Fatura",
            # "params": {
            #     "id": invoice_id,
            #     "action": 232,
            #     "cids": 2,
            #     "active_id": 7489,
            #     "menu_id": 246,
            #     "model": "account.move",
            #     "view_type": "form",
            # }
        }
        params = {
            "move_types": "",
            "composition_mode": "1",
            "invoice_ids": "1",
            "email_from": "1",
            "mail_server_id": "1",
            "is_print": "",
            "invalid_addresses": "",
            "snailmail_is_letter": "1",
            "snailmail_cost": "",
            "partner_id": "",
            "is_email": "1",
            "invoice_without_email": "",
            "partner_ids": "1",
            "subject": "1",
            "body": "1",
            "attachment_ids": "1",
            "template_id": "1",
        }
        response = self.execute_action_onchange(
            "account.invoice.send", params, extra_context=extra_context
        )
        return response
