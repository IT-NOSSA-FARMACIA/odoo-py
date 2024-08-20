from ._integration import OdooIntegration


class ProductModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_by_id(self, product_id):
        response = self.read("product.product", [product_id])
        return response

    def get_product_id_by_reference(self, reference_id):
        response = self.search(
            "product.product", [[["default_code", "=", reference_id]]]
        )
        if response:
            return response[0]
        raise Exception(f"Product '{reference_id}' not found")

 