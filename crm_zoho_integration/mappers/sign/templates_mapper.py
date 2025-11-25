import frappe
from crm_zoho_integration.mappers import utils


def get_template_doc(template_data):
    documents = []
    for document_data in template_data.get("document_ids"):
        documents.append(
            {
                "document_name": document_data.get("document_name"),
                "document_size": document_data.get("document_size"),
                "document_order": document_data.get("document_order"),
                "total_pages": document_data.get("total_pages"),
                "document_id": document_data.get("document_id"),
            }
        )

    actions = []
    for action_data in template_data.get("actions"):
        recipient_phone_number = ""
        if action_data.get("recipient_countrycode") and action_data.get(
            "recipient_phonenumber"
        ):
            recipient_phone_number = f"{action_data.get('recipient_countrycode')} {action_data.get('recipient_phonenumber')}"
        actions.append(
            {
                "verify_recipient": action_data.get("verify_recipient"),
                "action_id": action_data.get("action_id"),
                "action_type": action_data.get("action_type"),
                "private_notes": action_data.get("private_notes"),
                "recipient_email": action_data.get("recipient_email"),
                "signing_order": action_data.get("signing_order"),
                "recipient_name": action_data.get("recipient_name"),
                "recipient_phone_number": recipient_phone_number,
                "role": action_data.get("role"),
                "verification_type": action_data.get("verification_type"),
            }
        )

    return frappe.get_doc(
        {
            "doctype": "ZohoSign Template",
            "owner_email": template_data.get("owner_email"),
            "template_created_on": utils.timestamp_to_datetime(
                template_data.get("created_time")
            ),
            "email_reminders": template_data.get("email_reminders"),
            "documents": documents,
            "notes": template_data.get("notes"),
            "reminder_period": template_data.get("reminder_period"),
            "owner_id": template_data.get("document_id"),
            "description": template_data.get("description"),
            "template_name": template_data.get("template_name"),
            "template_modified_on": utils.timestamp_to_datetime(
                template_data.get("modified_time")
            ),
            "is_deleted": template_data.get("is_deleted"),
            "template_id": template_data.get("template_id"),
            "request_type_id": template_data.get("request_type_id"),
            "request_type_name": template_data.get("request_type_name"),
            "owner_first_name": template_data.get("owner_first_name"),
            "owner_last_name": template_data.get("owner_last_name"),
            "actions": actions,
            "is_sequential": template_data.get("is_sequential"),
            "expiration_days": template_data.get("expiration_days"),
        }
    )
