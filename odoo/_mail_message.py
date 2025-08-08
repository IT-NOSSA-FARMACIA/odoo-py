from ._integration import OdooIntegration


class MailMessageModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_mail_message(self, message_id):
        response = self.read("mail.message", [message_id])
        return response
