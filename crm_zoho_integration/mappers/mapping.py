from frappe import cint
from crm_zoho_integration.mappers.utils import timestamp_to_datetime
from crm_zoho_integration.mappers.field_types import FieldTypes


def apply_mapping(data: dict, mappings: dict) -> dict:
    result = {}
    country_codes = {}
    phone_fields = []

    for source_field, config in mappings.items():
        if source_field not in data:
            continue

        value = data.get(source_field)
        target_field = config.get("target_field")

        if config["type"] == FieldTypes.TIMESTAMP and value:
            result[target_field] = timestamp_to_datetime(value)

        elif config["type"] == FieldTypes.LIST and isinstance(value, list):
            item_mapping = config.get("item_mapping")
            if item_mapping:
                result[target_field] = [
                    apply_mapping(item, item_mapping) for item in value
                ]
            else:
                result[target_field] = value

        elif config["type"] == FieldTypes.DICT and isinstance(value, dict):
            item_mapping = config.get("item_mapping")
            if item_mapping:
                result[target_field] = apply_mapping(value, item_mapping)
            else:
                result[target_field] = value

        elif config["type"] == FieldTypes.COUNTRY_CODE:
            country_codes[source_field] = value

            if target_field:
                result[target_field] = value
        elif config["type"] == FieldTypes.PHONE_NUMBER:
            if value and config.get("country_code_field"):
                phone_fields.append({"value": value, **config})
        elif config["type"] == FieldTypes.INTEGER:
            result[target_field] = cint(value or "")
        elif config["type"] == FieldTypes.DOUBLE:
            result[target_field] = float(value or "0")
        else:
            result[target_field] = value

    for phone_field in phone_fields:
        country_code = country_codes.get(phone_field.get("country_code_field"))
        target_field = phone_field.get("target_field")
        phone_number = phone_field.get("value")

        if country_code:
            result[target_field] = f"{country_code} {phone_number}"
        else:
            result[target_field] = phone_number

    return result
