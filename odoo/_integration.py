from environs import Env
import xmlrpc.client

env = Env()
env.read_env()


class OdooIntegration:
    def __init__(
        self,
        odoo_url: str = None,
        odoo_db: str = None,
        odoo_username: str = None,
        odoo_password: str = None,
        odoo_language: str = None,
    ):
        self._url = odoo_url or env.str("ODOO_URL")
        self._db = odoo_db or env.str("ODOO_DB")
        self._username = odoo_username or env.str("ODOO_USERNAME")
        self._password = odoo_password or env.str("ODOO_PASSWORD")
        self._language = odoo_language or env.str("ODOO_LANGUAGE", default="es_ES")
        self._common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(self._url))
        self._uid = self._common.authenticate(
            self._db, self._username, self._password, {}
        )
        self._models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(self._url))

    def search(self, model: str, search_params: list):
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            "search",
            search_params,
            {"context": {"lang": self._language}},
        )
        return response

    def search_read(
        self,
        model: str,
        search_params: list,
        fields: list = None,
        limit: int = 10,
        offset: int = 0,
    ):
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            "search_read",
            search_params,
            {
                "fields": fields or [],
                "limit": limit,
                "offset": offset,
                "context": {"lang": self._language},
            },
        )
        return response

    def search_count(self, model: str, search_params: list):
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            "search_count",
            search_params,
            {"context": {"lang": self._language}},
        )
        return response

    def read(self, model: str, ids: list, fields: list = None):
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            "read",
            ids,
            {"fields": fields or [], "context": {"lang": self._language}},
        )
        return response

    def create(self, model: str, data: list[dict]):
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            "create",
            data,
            {"context": {"lang": self._language}},
        )
        return response

    def update(self, model: str, object_id: int, data: dict[str, any]):
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            "write",
            [[object_id], data],
            {"context": {"lang": self._language}},
        )
        return response

    def execute_action(self, model: str, action_type: str, object_id: int):
        response = self._models.execute_kw(
            self._db,
            self._uid,
            self._password,
            model,
            action_type,
            [[object_id]],
            {"context": {"lang": self._language}},
        )
        return response
