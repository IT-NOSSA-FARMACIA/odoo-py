from ._integration import OdooIntegration


class AnalyticAccountModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_analytic_account_id_by_name(self, analytic_account_name):
        response = self.search("account.analytic.account", [[["name", "=", analytic_account_name]]])
        if response:
            return response[0]
        raise Exception(f"Analytic account name '{analytic_account_name}' not found")
