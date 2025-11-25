import frappe
from crm_zoho_integration.services import sign_service


FETCH_TEMPLATES_TIMEOUT = 25 * 60
FETCH_TEMPLATES_JOB_NAME = "fetch_zohosign_templates"
FETCH_TEMPLATES_PROGRESS_EVENT = "fetch_zohosign_templates_progress"


@frappe.whitelist()
def fetch_templates():
    if not frappe.has_permission("ZohoSign Template", "create"):
        frappe.throw("User does not have permission to create new ZohoSign Template")

    frappe.enqueue(
        sign_service.sync_templates,
        queue="default",
        timeout=FETCH_TEMPLATES_TIMEOUT,
        job_name=FETCH_TEMPLATES_JOB_NAME,
        publish_progress=FETCH_TEMPLATES_PROGRESS_EVENT,
    )
    return {
        "status": "success",
        "msg": "ZohoSign Templates syncing started in background.",
        "track_on": FETCH_TEMPLATES_PROGRESS_EVENT,
    }
