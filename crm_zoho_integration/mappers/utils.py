import frappe


def timestamp_to_datetime(timestamp_in_ms: int | str):
    if isinstance(timestamp_in_ms, str):
        timestamp_in_ms = int(timestamp_in_ms)

    if not timestamp_in_ms:
        return None

    return frappe.utils.datetime.datetime.fromtimestamp(ms_to_seconds(timestamp_in_ms))


def ms_to_seconds(milliseconds):
    return milliseconds / 1000
