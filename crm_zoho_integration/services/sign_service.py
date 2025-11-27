import frappe
from . import auth_service
from crm_zoho_integration import utils
from crm_zoho_integration.integration.sign import sign_client
from crm_zoho_integration.mappers.sign import mappers

FETCH_ROW_COUNT = 25


def get_sign_webhook_url() -> str:
    return utils.get_absolute_url(
        "/api/method/crm_zoho_integration.webhook.sign.handle_document_event"
    )


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


def use_template(template_id: str, template_data: dict, quick_send: bool = True) -> str:
    if not frappe.has_permission("ZohoSign Template"):
        frappe.throw("User don't have permission to access ZohoSign Template.")
    if not frappe.has_permission("ZohoSign Document", "create"):
        frappe.throw("User don't have permission to create ZohoSign Document")

    zoho_settings = utils.get_zoho_settings()
    template_doc = frappe.get_doc("ZohoSign Template", template_id)

    template_payload = mappers.create_use_template_payload(
        template_doc, **template_data
    )

    document_data = sign_client.use_template(
        template_id=template_doc.template_id,
        template_payload=template_payload,
        quick_send=quick_send,
        access_token=auth_service.get_access_token(),
        server_domain=zoho_settings.server_domain,
    )
    document_doc = mappers.get_document_doc(document_data)
    document_doc.set("from_template", template_doc.name)
    document_doc.save()

    return document_doc.name
