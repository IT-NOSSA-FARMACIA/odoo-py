from ._integration import OdooIntegration


class IRAttachmentModel(OdooIntegration):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_ir_attachment(self, attachment_id):
        response = self.read("ir.attachment", [attachment_id])
        return response
