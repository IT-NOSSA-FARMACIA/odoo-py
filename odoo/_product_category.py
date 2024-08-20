from ._integration import OdooIntegration


class ProductCategoryModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_category_id_by_name(self, category_name):
        response = self.search("product.category", [[["name", "=", category_name]]])
        if response:
            return response[0]
        raise Exception(f"Tax '{category_name}' not found")
