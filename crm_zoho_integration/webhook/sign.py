import frappe
from crm_zoho_integration import decorators
from crm_zoho_integration.mappers.sign import mappers
import typing

if typing.TYPE_CHECKING:
    from frappe.model.document import Document


@frappe.whitelist(allow_guest=True)
@decorators.verify_zoho_hmac(secret_key_field="sign_hmac_key")
def handle_document_event(*args, **kwargs):
    frappe.enqueue(_handle_document_event, is_async=True, webhook_data=frappe.form_dict)


def _handle_document_event(webhook_data):
    document_data = webhook_data.get("requests")
    event_details = webhook_data.get("notifications")

    if not (document_data and event_details):
        frappe.throw("Invalid Request. Required data not found.")

    updated_document = mappers.get_document_doc(document_data, as_dict=True)
    activity_doc = mappers.get_document_activities_doc(event_details, as_dict=True)

    existing_document = frappe.db.exists(
        "ZohoSign Document", {"document_id": updated_document.get("document_id")}
    )
    document_doc = None
    if existing_document:
        document_doc = frappe.get_doc("ZohoSign Document", existing_document)
        if do_activity_already_exists(document_doc, activity_doc):
            return
    else:
        document_doc = frappe.new_doc("ZohoSign Document")

    document_doc.update(updated_document)
    document_doc.append("document_activities", activity_doc)

    frappe.set_user("Administrator")
    if document_doc.document_status == "completed":
        document_doc.sign_percentage = 100
        document_doc.submit()
    else:
        document_doc.save()

    frappe.db.commit()


def do_activity_already_exists(document_doc: "Document", activity: dict) -> bool:
    for doc_activity in document_doc.document_activities:
        if (
            doc_activity.get("performed_from") == activity.get("performed_from")
            and doc_activity.get("operation_type") == activity.get("operation_type")
            and frappe.utils.get_datetime(activity.get("performed_at"))
            == frappe.utils.get_datetime(doc_activity.get("performed_at"))
        ):
            return True

    return False
