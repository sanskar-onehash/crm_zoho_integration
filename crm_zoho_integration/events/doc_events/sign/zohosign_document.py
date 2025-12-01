import typing
from crm_zoho_integration.services import sign_service

if typing.TYPE_CHECKING:
    from frappe.model.document import Document


def before_submit(doc: "Document", method: str | None = None):
    doc = sign_service.download_document_pdf(doc, True)
