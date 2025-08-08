from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class IRAttachmentModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_ir_attachment(self, attachment_id: int) -> list[dict[str, Any]]:
        response = self.read("ir.attachment", [attachment_id])
        return response
