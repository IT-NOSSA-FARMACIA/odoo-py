from ._integration import OdooIntegration


class SaleOrderModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_sale_order_by_any_filter(self, filter: list):
        response = self.search("sale.order", [filter])
        return response

    def get_sale_order_by_state(self, state: list):
        response = self.search("sale.order", [[["state", "in", state]]])
        return response

    def get_sale_order_by_id(self, sale_order_id, fields=None):
        response = self.read("sale.order", [sale_order_id], fields)
        return response

    def get_sale_order_line_list_by_sale_order_id(self, sale_order_id):
        response = self.search("sale.order.line", [[["order_id", "=", sale_order_id]]])
        return response

    def get_sale_order_line_by_id(self, sale_order_line_id):
        response = self.read("sale.order.line", [sale_order_line_id])
        return response

    def create_sale_order_line(self, sale_order_line_data: dict):
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

    def create_sale_order(self, sale_order_data: dict):
        # sale_order = {
        #     "partner_id": partner_id,
        #     "company_id": company_id,  # serão duas empresas, addo pharm e addo pharm distribuição
        #     "warehouse_id": warehouse_id,  # warehouse de distribuiçãos (armazem)
        #     "analytic_account_id": analytic_account_id,
        # }
        response = self.create("sale.order", [sale_order_data])
        return response

    def confirm_sale_order(self, sale_order_id):
        response = self.execute_action("sale.order", "action_confirm", sale_order_id)
        return response

    def certify_sale_order(self, sale_order_id):
        response = self.execute_action("sale.order", "certify", sale_order_id)
        return response
