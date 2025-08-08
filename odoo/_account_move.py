from ._integration import OdooIntegration


class AccountMoveModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def confirm_invoice_purchase_order(self, invoice_id: int):
        response = self.execute_action("account.move", "action_post", invoice_id)

    def invoice_insert_footer_notes(self, invoice_id: int, notes: str):
        response = self.update("account.move", invoice_id, {"footer_notes": notes})
        return response

    def invoice_insert_product_line(self, invoice_id: int, data: dict):
        response = self.update("account.move", invoice_id, data)
        return response

    def get_invoice_by_id(self, invoice_id: int):
        response = self.read("account.move", [invoice_id])
        return response

    def get_invoice_line_by_id(self, account_move_line_id: int):
        response = self.read("account.move.line", [account_move_line_id])
        return response

    def update_invoice_line(self, invoice_id: int, data: dict):
        response = self.update("account.move", invoice_id, data)
        return response

    def get_account_move_line_by_id(self, account_move_line_id: int):
        response = self.read("account.move.line", [account_move_line_id])
        return response

    def get_account_move_by_id(self, account_move_id: int, fields: list = None):
        response = self.read("account.move", [account_move_id], fields=fields)
        return response

    def create_account_move(self, account_move_data: dict):
        response = self.create("account.move", [account_move_data])
        return response

    def create_account_move_line(self, account_move_line_data: dict):
        response = self.create("account.move.line", [account_move_line_data])
        return response

    def update_account_move_line(self, account_move_line_id: int, data: dict):
        response = self.update("account.move.line", account_move_line_id, data)
        return response

    def update_account_move(self, account_move_id: int, data: dict):
        response = self.update("account.move", account_move_id, data)
        return response

    def confirm_account_move(self, account_move_id: int):
        response = self.execute_action("account.move", "action_post", account_move_id)
        return response
    
    def create_account_payment_register(self, data: dict, context: dict = None):
        response = self.create("account.payment.register", [data], context)
        return response

    def execute_action_create_payments(self, account_payment_register_id: int, context: dict = None):
        response = self.execute_action("account.payment.register", "action_create_payments", account_payment_register_id, context)
        return response
