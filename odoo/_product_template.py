from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class ProductTemplateModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _validate_detailed_type(self, detailed_type: str) -> None:
        """
        product = Artigo Armazenável
        consul = Consumível
        service = Serviço
        """
        if detailed_type not in ["product", "consul", "service"]:
            raise Exception("Detailed type not valid")

    def _validate_invoice_policy(self, invoice_policy: str) -> None:
        """
        orders = Quantidades Pedidas
        delivery = Quantidades Entregues
        """
        if invoice_policy not in ["order", "delivery"]:
            raise Exception("Invoice policy not valid")

    def _validate_expense_policy(self, expense_policy: str) -> None:
        """
        no = Não
        cost = A Custo
        sales_price = Preço de vendas
        """
        if expense_policy not in ["no", "cost", "sales_price"]:
            raise Exception("Expense policy not valid")

    def _validate_tracking(self, tracking: str | None) -> None:
        """
        none = Sem rastreio
        lot = Por Lotes
        serial = Por número de série
        """
        if tracking not in ["lot", "serial", None]:
            raise Exception("Tracking not valid")

    def _validate_purchase_method(self, purchase_method: str) -> None:
        """
        receive = Nas quantidades recebidas
        purchase = Nas quantidades pedidas
        """
        if purchase_method not in ["purchase", "receive"]:
            raise Exception("Purchase method not valid")

    def get_product_by_id(self, product_id: int) -> list[dict[str, Any]]:
        response = self.read("product.template", [product_id])
        return response

    def get_product_id_by_reference(self, reference_id: str) -> int:
        response = self.search(
            "product.template", [[["default_code", "=", reference_id]]]
        )
        if response:
            return response[0]
        raise Exception(f"Product '{reference_id}' not found")

    def create_product(
        self,
        name: str,
        default_code: str,
        detailed_type: str,
        invoice_policy: str,
        expense_policy: str,
        list_price: float,
        taxes_id: list[int],
        standard_price: float,
        categ_id: int,
        tracking: str | None,
        purchase_method: str,
        supplier_taxes_id: list[int],
        use_expiration_date: bool = True,
        sale_ok: bool = True,
        purchase_ok: bool = True,
        barcode: str | None = None,
    ) -> int | list[int]:
        self._validate_detailed_type(detailed_type)
        self._validate_invoice_policy(invoice_policy)
        self._validate_expense_policy(expense_policy)
        self._validate_tracking(tracking)
        self._validate_purchase_method(purchase_method)

        product_data = {
            "name": name,
            "default_code": default_code,
            "detailed_type": detailed_type,
            "invoice_policy": invoice_policy,
            "expense_policy": expense_policy,
            "list_price": list_price,
            "taxes_id": taxes_id,
            "standard_price": standard_price,
            "categ_id": categ_id,
            "tracking": tracking,
            "purchase_method": purchase_method,
            "supplier_taxes_id": supplier_taxes_id,
            "use_expiration_date": use_expiration_date,
            "sale_ok": sale_ok,
            "purchase_ok": purchase_ok,
            "barcode": barcode if barcode else False,
        }
        response = self.create("product.template", [product_data])
        return response
