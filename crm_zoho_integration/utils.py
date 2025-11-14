import frappe
from frappe import utils


def get_zoho_settings(throw=True):
    zoho_settings = frappe.get_doc("Zoho Settings")

    if throw and not zoho_settings.enabled:
        frappe.throw("Zoho Settings is not enabled.")

    return zoho_settings


def get_zoho_base_uri():
    zoho_settings = get_zoho_settings()
    return zoho_settings.api_base_uri


def get_absolute_url(path):
    return utils.get_url() + path
