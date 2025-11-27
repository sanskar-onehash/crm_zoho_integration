import frappe
from crm_zoho_integration import decorators
from crm_zoho_integration.mappers.sign import mappers


@frappe.whitelist(allow_guest=True)
@decorators.verify_zoho_hmac(secret_key_field="sign_hmac_key")
def handle_document_event(*args, **kwargs):
    document_data = frappe.form_dict.get("requests")
    event_details = frappe.form_dict.get("notifications")

    updated_document = mappers.get_document_doc(document_data, as_dict=True)
    activity_doc = mappers.get_document_activities_doc(event_details, as_dict=True)

    existing_document = frappe.db.exists(
        "ZohoSign Document", {"document_id": updated_document.get("document_id")}
    )
    document_doc = None

    if existing_document:
        document_doc = frappe.get_doc("ZohoSign Document", existing_document)
    else:
        document_doc = frappe.new_doc("ZohoSign Document")

    document_doc.update(updated_document)
    document_doc.append("document_activities", activity_doc)
    document_doc.save(ignore_permissions=True)

    frappe.db.commit()
