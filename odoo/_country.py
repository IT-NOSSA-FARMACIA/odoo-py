from ._integration import OdooIntegration


class CountryModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_country_id_by_code(self, country_code):
        response = self.search("res.country", [[["code", "=", country_code]]])
        if response:
            return response[0]
        raise Exception(f"Country '{country_code}' not found")
    
    def get_country_id_by_name(self, country_name):
        response = self.search("res.country", [[["name", "=", country_name]]])
        if response:
            return response[0]
        raise Exception(f"Country '{country_name}' not found")

    def get_country_state_by_id(self, state_id):
        response = self.read("res.country.state", [state_id])
        if response:
            return response[0]
        raise Exception(f"State '{state_id}' not found")

    def get_country_state_id_by_name(self, state_name):
        response = self.search("res.country.state", [[["name", "=", state_name]]])
        if response:
            return response[0]
        raise Exception(f"State '{state_name}' not found")
