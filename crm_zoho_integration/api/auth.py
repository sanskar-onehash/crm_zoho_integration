import frappe
from crm_zoho_integration.services import auth_service


@frappe.whitelist()
def get_auth_url():
    return auth_service.get_auth_url()


@frappe.whitelist(allow_guest=True)
def verify_auth(code, location):
    auth_service.generate_access_token(code, location)

    frappe.db.commit()

    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = frappe.utils.get_url_to_list("Zoho Settings")
