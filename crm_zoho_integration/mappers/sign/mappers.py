import frappe
from crm_zoho_integration.mappers.field_types import FieldTypes
from crm_zoho_integration.mappers.mapping import apply_mapping
from . import mappings


def get_template_doc(template_data: dict, as_dict=False):
    template_doc_data = apply_mapping(template_data, mappings.TEMPLATE_TO_DOC_MAP)
    return (
        template_doc_data
        if as_dict
        else frappe.get_doc({"doctype": "ZohoSign Template", **template_doc_data})
    )


def get_document_doc(document_data: dict, as_dict=False):
    document_doc_data = apply_mapping(document_data, mappings.DOCUMENT_TO_DOC_MAP)
    return (
        document_doc_data
        if as_dict
        else frappe.get_doc({"doctype": "ZohoSign Document", **document_doc_data})
    )


def get_document_activities_doc(activities_data: dict, as_dict=False):
    document_doc_data = apply_mapping(
        activities_data, mappings.DOCUMENT_ACTIVITES_TO_DOC_MAP
    )
    return (
        document_doc_data
        if as_dict
        else frappe.get_doc({"doctype": "ZohoSign Document", **document_doc_data})
    )


def create_use_template_payload(
    template_doc,
    document_name: str,
    actions: list[dict],
    field_data: dict | None = {},
    notes: str | None = None,
) -> dict:
    """
    Create a payload for using a ZohoSign template.

    Parameters:
        template_doc (ZohoSignTemplate): The template document to be used.
        document_name (str): The name of the document.
        field_data (dict): A dictionary containing data for different types of fields in the template.
            The dictionary can include:
            - `field_text_data`: A dictionary of text field values.
            - `field_boolean_data`: A dictionary of boolean field values.
            - `field_date_data`: A dictionary of date field values.
        actions (list[ZohoSignDocumentActions|dict]): A list of actions that define how the template will be used.
            Each action is a dictionary or ZohoSignDocumentActions doc that includes recipient information, action type, etc.
        notes (str|None): Optional notes to include with the payload.

    Return:
        dict: A dictionary representing the payload with the provided data.

    Documentation:
        For more information on using ZohoSign Template refer:
        `https://www.zoho.com/sign/api/template-managment/send-documents-using-template.html`
    """

    if len(actions) != len(template_doc.actions):
        frappe.throw("Action Items doesn't match with Template actions.")

    if field_data is None:
        field_data = {}

    valid_action_keys = mappings.DOCUMENT_ACTIONS_TO_DOC_MAP.keys()
    parsed_actions = []

    for idx, action in enumerate(actions):
        if action["action_type"] != template_doc.actions[idx].get("action_type"):
            frappe.throw("Action Items doesn't match with Template actions.")

        parsed_action = {}
        for key in valid_action_keys:
            value = action.get(key) or ""

            if (
                mappings.DOCUMENT_ACTIONS_TO_DOC_MAP[key].get("type")
                == FieldTypes.BOOLEAN
            ):
                # Convert frappe's cint into bool
                value = bool(value)

            parsed_action[key] = value

        if action.get("recipient_phone_number"):
            phone_number_parts = action.get("recipient_phone_number").split(" ")
            if len(phone_number_parts) < 2:
                frappe.throw("Invalid phone number format")

            parsed_action["recipient_countrycode"] = phone_number_parts[0]
            parsed_action["recipient_phonenumber"] = "".join(phone_number_parts[1:])

        parsed_actions.append(parsed_action)

    return {
        "request_name": document_name,
        "field_data": field_data,
        "actions": parsed_actions,
        "notes": notes,
    }
