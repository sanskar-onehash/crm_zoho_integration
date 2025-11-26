import frappe
from crm_zoho_integration.mappers.mapping import apply_mapping
from . import mappings


def get_template_doc(template_data: dict) -> frappe.Document:
    template_doc_data = apply_mapping(template_data, mappings.TEMPLATE_TO_DOC_MAP)
    return frappe.get_doc({"doctype": "ZohoSign Template", **template_doc_data})
