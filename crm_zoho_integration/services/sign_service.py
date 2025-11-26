import frappe
from . import auth_service
from crm_zoho_integration import utils
from crm_zoho_integration.integration.sign import sign_client
from crm_zoho_integration.mappers.sign import mappers

FETCH_ROW_COUNT = 25


def sync_templates(publish_progress: None) -> None:
    zoho_settings = utils.get_zoho_settings()
    start_index = 0

    while True:
        templates_data = sign_client.fetch_templates(
            server_domain=zoho_settings.server_domain,
            access_token=auth_service.get_access_token(),
            row_count=FETCH_ROW_COUNT,
            start_index=start_index,
        )

        for idx, template in enumerate(templates_data.get("templates")):
            if publish_progress:
                frappe.publish_realtime(
                    publish_progress,
                    {
                        "progress": idx + 1,
                        "total": templates_data.get("total_count"),
                        "title": "Fetching ZohoSign Templates",
                    },
                )

            if not frappe.db.exists(
                "ZohoSign Template", {"template_id": template.get("template_id")}
            ):
                mappers.get_template_doc(template).save()

        if templates_data.get("has_more_rows"):
            start_index = start_index + FETCH_ROW_COUNT - 1
        else:
            break

    frappe.db.commit()
