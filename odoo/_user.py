from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class UserModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_user_by_id(
        self, user_id: int, fields: list[str] | None = None
    ) -> dict[str, Any]:
        response = self.read("res.users", [user_id], fields)
        if response:
            return response[0]
        raise Exception(f"User '{user_id}' not found")

    def get_user_id_by_name(self, username: str) -> int:
        response = self.search("res.users", [[["name", "=", username]]])
        if response:
            return response[0]
        raise Exception(f"User '{username}' not found")
