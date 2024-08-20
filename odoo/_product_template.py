from ._integration import OdooIntegration


class ProductTemplateModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _validate_detailed_type(self, detailed_type):
        """
        product = Artigo Armazenável
        consul = Consumível
        service = Serviço
        """
        if detailed_type not in ["product", "consul", "service"]:
            raise Exception("Detailed type not valid")

    def _validate_invoice_policy(self, invoice_policy):
        """
        orders = Quantidades Pedidas
        delivery = Quantidades Entregues
        """
        if invoice_policy not in ["order", "delivery"]:
            raise Exception("Invoice policy not valid")

    def _validate_expense_policy(self, expense_policy):
        """
        no = Não
        cost = A Custo
        sales_price = Preço de vendas
        """
        if expense_policy not in ["no", "cost", "sales_price"]:
            raise Exception("Expense policy not valid")

    def _validate_tracking(self, tracking):
        """
        none = Sem rastreio
        lot = Por Lotes
        serial = Por número de série
        """
        if tracking not in ["lot", "serial", None]:
            raise Exception("Tracking not valid")

    def _validate_purchase_method(self, purchase_method):
        """
        receive = Nas quantidades recebidas
        purchase = Nas quantidades pedidas
        """
        if purchase_method not in ["purchase", "receive"]:
            raise Exception("Purchase method not valid")

    def get_product_by_id(self, product_id):
        response = self.read("product.template", [product_id])
        return response

    def get_product_id_by_reference(self, reference_id):
        response = self.search(
            "product.template", [[["default_code", "=", reference_id]]]
        )
        if response:
            return response[0]
        raise Exception(f"Product '{reference_id}' not found")

    def create_product(
        self,
        name,
        default_code,
        detailed_type,
        invoice_policy,
        expense_policy,
        list_price,
        taxes_id,
        standard_price,
        categ_id,
        tracking,
        purchase_method,
        supplier_taxes_id,
        use_expiration_date=True,
        sale_ok=True,
        purchase_ok=True,
        barcode=None,
    ):
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
