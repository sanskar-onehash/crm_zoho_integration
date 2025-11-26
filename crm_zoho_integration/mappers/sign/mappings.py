from werkzeug.local import F
from crm_zoho_integration.mappers.field_types import FieldTypes

TEMPLATE_DOCUMENTS_TO_DOC_MAP = {
    "document_name": {
        "target_field": "document_name",
        "type": FieldTypes.STRING,
    },
    "document_size": {
        "target_field": "document_size",
        "type": FieldTypes.INTEGER,
    },
    "document_order": {
        "target_field": "ocument_order",
        "type": FieldTypes.INTEGER,
    },
    "total_pages": {
        "target_field": "total_pages",
        "type": FieldTypes.INTEGER,
    },
    "document_id": {
        "target_field": "document_id",
        "type": FieldTypes.STRING,
    },
}

DOCUMENT_ACTIONS_TO_DOC_MAP = {
    "verify_recipient": {
        "target_field": "verify_recipient",
        "type": FieldTypes.STRING,
    },
    "action_id": {
        "target_field": "action_id",
        "type": FieldTypes.STRING,
    },
    "action_type": {
        "target_field": "action_type",
        "type": FieldTypes.STRING,
    },
    "private_notes": {
        "target_field": "private_notes",
        "type": FieldTypes.STRING,
    },
    "recipient_email": {
        "target_field": "recipient_email",
        "type": FieldTypes.STRING,
    },
    "signing_order": {
        "target_field": "signing_order",
        "type": FieldTypes.STRING,
    },
    "recipient_name": {
        "target_field": "recipient_name",
        "type": FieldTypes.STRING,
    },
    "recipient_countrycode": {
        "type": FieldTypes.COUNTRY_CODE,
    },
    "recipient_phonenumber": {
        "target_field": "recipient_phone_number",
        "type": FieldTypes.PHONE_NUMBER,
        "country_code_field": "recipient_countrycode",
    },
    "role": {
        "target_field": "role",
        "type": FieldTypes.STRING,
    },
    "verification_type": {
        "target_field": "verification_type",
        "type": FieldTypes.STRING,
    },
}

TEMPLATE_TO_DOC_MAP = {
    "document_name": {"target_field": "document_name", "type": FieldTypes.STRING},
    "document_size": {"target_field": "document_size", "type": FieldTypes.INTEGER},
    "document_order": {"target_field": "document_order", "type": FieldTypes.INTEGER},
    "total_pages": {"target_field": "total_pages", "type": FieldTypes.INTEGER},
    "document_id": {"target_field": "document_id", "type": FieldTypes.STRING},
    "owner_email": {"target_field": "owner_email", "type": FieldTypes.STRING},
    "template_created_on": {
        "target_field": "template_created_on",
        "type": FieldTypes.TIMESTAMP,
    },
    "template_modified_on": {
        "target_field": "template_modified_on",
        "type": FieldTypes.TIMESTAMP,
    },
    "actions": {
        "target_field": "actions",
        "type": FieldTypes.LIST,
        "item_mapping": DOCUMENT_ACTIONS_TO_DOC_MAP,
    },
    "is_sequential": {"target_field": "is_sequential", "type": FieldTypes.BOOLEAN},
    "expiration_days": {"target_field": "expiration_days", "type": FieldTypes.INTEGER},
}
