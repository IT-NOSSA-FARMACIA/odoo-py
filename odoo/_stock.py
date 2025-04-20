from ._integration import OdooIntegration
from .exceptions import LotProductNotFoundError, TooManyLotProducError


class StockModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_lot_id_by_serie_name(self, serie_name):
        response = self.search("stock.production.lot", [[["name", "=", serie_name]]])
        if response:
            return response[0]
        raise Exception(f"Product Lot '{serie_name}' not found")

    def get_product_lot_id_by_serie_name_and_product_id(
        self, serie_name, product_id: int, company_id: int = None
    ):
        if company_id:
            search_params = [
                [
                    ["name", "=", serie_name],
                    ["product_id", "=", product_id],
                    ["company_id", "=", company_id],
                ]
            ]
        else:
            search_params = [
                [["name", "=", serie_name], ["product_id", "=", product_id]]
            ]
        response = self.search("stock.production.lot", search_params)
        if len(response) > 1:
            raise TooManyLotProducError(
                f"Multiple Product Lots with name '{serie_name}' found"
            )
        if response:
            return response[0]
        raise LotProductNotFoundError(f"Product Lot '{serie_name}' not found")

    def get_product_lot_by_id(self, product_lot_id):
        response = self.read("stock.production.lot", [product_lot_id])
        return response

    def get_warehouse_id_by_name(self, warehouse_name, company_id):
        response = self.search(
            "stock.warehouse",
            [[["name", "=", warehouse_name], ["company_id", "=", company_id]]],
        )
        if response:
            return response[0]
        raise Exception(f"Warehouse '{warehouse_name}' not found")

    def get_warehouse_by_id(self, warehouse_id):
        response = self.read("stock.warehouse", [warehouse_id])
        return response

    def create_product_lot(
        self,
        product_id,
        serie_number,
        company_id,
        expiration_date,
        removal_date,
        alert_date,
        use_date,
        product_uom_id=1,
    ):
        product_lot = {
            "product_id": product_id,
            "name": serie_number,
            "company_id": company_id,
            # "product_qty": product_qty,
            "product_uom_id": product_uom_id,  # unidade de medida - 1 é unidade
            "expiration_date": expiration_date,  # Data de Validade
            "removal_date": removal_date,  # Data de Remoção
            "alert_date": alert_date,  # Data de Alerta
            "use_date": use_date,  # Consumir antes da data
        }
        response = self.create("stock.production.lot", [product_lot])
        return response

    def get_picking_type_id_by_name(
        self, picking_type_name, company_id, warehouse_id=None
    ):
        query = [["name", "=", picking_type_name], ["company_id", "=", company_id]]
        if warehouse_id:
            query.append(["warehouse_id", "=", warehouse_id])
        response = self.search(
            "stock.picking.type",
            [query],
        )
        print(response)
        if not response:
            raise Exception(f"Picking Type '{picking_type_name}' not found")
        elif len(response) > 1:
            raise Exception(
                f"Multiple Picking Types with name '{picking_type_name}' found"
            )
        return response[0]

    def get_picking_type_id_by_id(self, picking_type_id):
        response = self.read("stock.picking.type", [picking_type_id])
        return response

    def get_picking_type_id_by_warehouse_id(self, warehouse_id):
        response = self.search(
            "stock.picking.type", [[["warehouse_id", "=", warehouse_id]]]
        )
        return response

    def get_picking_id_list_by_sale_order_id(self, sale_order_id):
        response = self.search("stock.picking", [[["sale_id", "=", sale_order_id]]])
        return response

    def get_picking_id_list_by_purchase_order_id(self, purchase_order_id):
        response = self.search(
            "stock.picking", [[["purchase_id", "=", purchase_order_id]]]
        )
        return response

    def get_picking_by_id(self, picking_id):
        response = self.read("stock.picking", [picking_id])
        return response

    def update_picking(self, picking_id, data):
        response = self.update("stock.picking", picking_id, data)
        return response

    def validate_picking(self, picking_id):
        response = self.execute_action("stock.picking", "button_validate", picking_id)
        return response

    def confirm_backorder(self, sale_order_id, picking_id, backorder_confirmation_id):
        extra_context = {
            "active_id": sale_order_id,
            "active_ids": [sale_order_id],
            "button_validate_picking_ids": [picking_id],
            "params": {
                "id": picking_id,
                "active_id": sale_order_id,
                "model": "stock.picking",
                "view_type": "form",
            },
            "contact_display": "partner_address",
            "active_model": "stock.picking",
        }
        response = self.execute_action(
            "stock.backorder.confirmation",
            "process_cancel_backorder",
            backorder_confirmation_id,
            extra_context,
        )
        return response

    def get_stock_picking_move_line_id_by_picking_id(self, picking_id):
        response = self.search("stock.move.line", [[["picking_id", "=", picking_id]]])
        return response

    def get_stock_picking_move_line(self, stock_move_line_id):
        response = self.read("stock.move.line", [stock_move_line_id])
        return response

    def confirm_picking(self, picking_data):
        response = self.create("stock.backorder.confirmation", picking_data)
        return response

    def unlink_picking(self, picking_id):
        response = self.execute_action("stock.picking", "unlink", picking_id)
        return response
