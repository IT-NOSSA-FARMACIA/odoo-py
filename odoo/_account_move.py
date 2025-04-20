from ._integration import OdooIntegration


class AccountMoveModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def confirm_invoice_purchase_order(self, invoice_id):
        response = self.execute_action("account.move", "action_post", invoice_id)

    def invoice_insert_footer_notes(self, invoice_id, notes):
        response = self.update("account.move", invoice_id, {"footer_notes": notes})
        return response

    def invoice_insert_product_line(self, invoice_id, data):
        response = self.update("account.move", invoice_id, data)
        return response

    def get_invoice_by_id(self, invoice_id):
        response = self.read("account.move", [invoice_id])
        return response

    def get_invoice_line_by_id(self, account_move_line_id):
        response = self.read("account.move.line", [account_move_line_id])
        return response
    
    def update_invoice_line(self, invoice_id, data):
        response = self.update("account.move", invoice_id, data)
        return response
