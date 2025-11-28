import frappe
from crm_zoho_integration.services import sign_service


FETCH_TEMPLATES_TIMEOUT = 25 * 60
FETCH_TEMPLATES_JOB_NAME = "fetch_zohosign_templates"
FETCH_TEMPLATES_PROGRESS_EVENT = "fetch_zohosign_templates_progress"


@frappe.whitelist()
def generate_hmac_secret():
    return frappe.generate_hash(length=128)


@frappe.whitelist()
def sync_template(template_name: str):
    return sign_service.sync_template(template_name)


@frappe.whitelist()
def fetch_templates():
    if not frappe.has_permission("ZohoSign Template", "create"):
        frappe.throw("User does not have permission to create new ZohoSign Template")

    frappe.enqueue(
        _fetch_templates,
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


def _fetch_templates(publish_progress: str):
    sign_service.sync_templates(publish_progress=publish_progress)
    frappe.db.commit()


@frappe.whitelist()
def use_template(template_id: str, template_data: str | dict):
    if isinstance(template_data, str):
        template_data = frappe.parse_json(template_data)

    return sign_service.use_template(template_id, template_data)
