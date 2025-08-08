from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class MailMessageModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_mail_message(self, message_id: int) -> list[dict[str, Any]]:
        response = self.read("mail.message", [message_id])
        return response
