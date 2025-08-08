from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class CRMTagModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_crm_tag_by_id(self, crm_tag_id: int) -> dict[str, Any]:
        response = self.read("res.partner.category", [crm_tag_id])
        if response:
            return response[0]
        raise Exception(f"CRM Label '{crm_tag_id}' not found")

    def get_crm_tag_id_by_name(self, crm_tag_name: str) -> int:
        response = self.search("crm.tag", [[["name", "=", crm_tag_name]]])
        if response:
            return response[0]
        raise Exception(f"CRM Label '{crm_tag_name}' not found")
