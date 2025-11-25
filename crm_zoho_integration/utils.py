import frappe


def get_zoho_settings(throw=True):
    zoho_settings = frappe.get_doc("Zoho Settings")

    if throw and not zoho_settings.enabled:
        frappe.throw("Zoho Settings is not enabled.")

    return zoho_settings


def get_absolute_url(path):
    return frappe.utils.get_url() + path
