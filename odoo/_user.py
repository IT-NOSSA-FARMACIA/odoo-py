from ._integration import OdooIntegration


class UserModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_user_by_id(self, user_id):
        response = self.read("res.users", [user_id])
        if response:
            return response[0]
        raise Exception(f"User '{user_id}' not found")

    def get_user_id_by_name(self, username):
        response = self.search("res.users", [[["name", "=", username]]])
        if response:
            return response[0]
        raise Exception(f"User '{username}' not found")
