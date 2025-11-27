import frappe
from crm_zoho_integration import utils


def verify_zoho_hmac(secret_key_field: str, signature_header="X-Zs-Webhook-Signature"):
    def decorator(fn):
        def innerfn(*args, **kwargs):
            if not secret_key_field:
                frappe.throw("Webhook not configured.")

            received_signature = frappe.request.headers.get(signature_header) or ""
            if not received_signature:
                frappe.throw("Unauthorized. No signature found.")

            zoho_settings = utils.get_zoho_settings()
            if not zoho_settings.get(secret_key_field):
                frappe.throw("Secret field not found.")

            secret_key = zoho_settings.get_password(secret_key_field) or ""
            if not isinstance(secret_key, str):
                secret_key = str(secret_key)

            raw_request_data = frappe.request.get_data()

            if not utils.verify_hmac(secret_key, raw_request_data, received_signature):
                frappe.throw("Unauthorized. Signature didn't matched.")

            return fn(*args, **kwargs)

        return innerfn

    return decorator
