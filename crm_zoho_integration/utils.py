import base64
import frappe
import hashlib
import hmac
import typing

if typing.TYPE_CHECKING:
    from frappe.model.document import Document


def get_zoho_settings(throw: bool = True):
    zoho_settings = frappe.get_doc("Zoho Settings")

    if throw and not zoho_settings.enabled:
        frappe.throw("Zoho Settings is not enabled.")

    return zoho_settings


def get_absolute_url(path: str):
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


def create_or_update(
    doctype: str,
    existing_doc_condition: str | dict | list,
    doc_data: dict,
    save: bool = False,
    ignore_permissions: bool = False,
) -> "Document":
    existing_doc = frappe.db.exists(doctype, existing_doc_condition)
    should_update = True

    doc = None
    if existing_doc:
        doc = frappe.get_doc(doctype, existing_doc)
        should_update = check_if_outdated(doc, doc_data)
    else:
        doc = frappe.new_doc(doctype)

    if should_update:
        doc.update(doc_data)

        if save:
            doc.save(ignore_permissions=ignore_permissions)

    return doc


def update_if_outdated(
    doc: "Document", data: dict, save: bool = False, ignore_permissions=False
) -> "Document":
    if check_if_outdated(doc, data):
        doc.update(data)
        if save:
            doc.save(ignore_permissions=ignore_permissions)
    return doc


def check_if_outdated(doc: "Document", data: dict) -> bool:
    is_outdated = False

    for key, value in data.items():
        doc_value = doc.get(key)

        if isinstance(value, list):
            if len(value) != len(doc_value):
                is_outdated = True
                break

            for idx, child in enumerate(value):
                is_outdated = check_if_outdated(doc_value[idx], child)
                if is_outdated:
                    break

        elif not (value or doc_value):
            # pass if both are falsy values
            pass
        elif value != doc_value:
            is_outdated = True

        if is_outdated:
            break

    return is_outdated
