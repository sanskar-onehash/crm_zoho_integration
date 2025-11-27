import frappe
import hmac
import hashlib
import base64


def get_zoho_settings(throw=True):
    zoho_settings = frappe.get_doc("Zoho Settings")

    if throw and not zoho_settings.enabled:
        frappe.throw("Zoho Settings is not enabled.")

    return zoho_settings


def get_absolute_url(path):
    return frappe.utils.get_url() + path


def verify_hmac(
    key: bytes | bytearray | str,
    value: bytes | bytearray | str | None,
    signature: str,
) -> bool:
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(value, str):
        value = value.encode("utf-8")

    computed_hmac = hmac.new(key, value, hashlib.sha256).digest()
    computed_signature = base64.b64encode(computed_hmac).decode("utf-8")

    return hmac.compare_digest(computed_signature, signature)
