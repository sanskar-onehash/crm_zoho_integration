import frappe
from crm_zoho_integration.config import sign_config


def after_install():
    add_zohosign_actions()

    frappe.db.commit()


def add_zohosign_actions():
    for action in sign_config.ZOHOSIGN_ACTIONS:
        if not frappe.db.exists("ZohoSign Action", action.get("action_id")):
            frappe.get_doc({"doctype": "ZohoSign Action", **action}).save()
