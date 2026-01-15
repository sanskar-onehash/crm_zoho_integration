import frappe
import typing
from frappe.utils import pdf as pdf_utils

from . import auth_service
from crm_zoho_integration import utils
from crm_zoho_integration.integration.sign import sign_client
from crm_zoho_integration.mappers.sign import mappers

if typing.TYPE_CHECKING:
    from frappe.model.document import Document

FETCH_ROW_COUNT = 25


def get_sign_webhook_url() -> str:
    return utils.get_absolute_url(
        "/api/method/crm_zoho_integration.webhook.sign.handle_document_event"
    )


def sync_template(template_name):
    template_id = frappe.db.get_value("ZohoSign Template", template_name, "template_id")
    if not template_id:
        frappe.throw("No Template found.")

    zoho_settings = utils.get_zoho_settings()

    template_data = sign_client.get_template(
        template_id=template_id,
        server_domain=zoho_settings.server_domain,
        access_token=auth_service.get_access_token(),
    )
    template_doc_data = mappers.get_template_doc(template_data, as_dict=True)

    utils.create_or_update(
        "ZohoSign Template",
        {"template_id": template_data.get("template_id")},
        template_doc_data,
        save=True,
    )


def sync_templates(publish_progress: bool = True) -> None:
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

            template_doc_data = mappers.get_template_doc(template, as_dict=True)

            utils.create_or_update(
                "ZohoSign Template",
                {"template_id": template.get("template_id")},
                template_doc_data,
                save=True,
            )

        if templates_data.get("has_more_rows"):
            start_index = start_index + FETCH_ROW_COUNT - 1
        else:
            break


def use_template(
    template_id: str, template_data: dict, quick_send: bool = True
) -> dict:
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

    return {"document_data": document_data, "doc": document_doc.as_dict()}


def add_document_by_html(
    document_id: str, file_name: str, file_content: str, document_order: int | None
):
    zoho_settings = utils.get_zoho_settings()
    sign_doc = frappe.get_doc("ZohoSign Document", {"document_id": document_id})

    if not sign_doc:
        frappe.throw("ZohoSign Document not found.")
    if not sign_doc.has_permission("write"):
        frappe.throw("You don't have permissions to perform this action.")

    if not file_name.endswith(".pdf"):
        file_name += ".pdf"

    file_content = pdf_utils.get_pdf(frappe.render_template(file_content, {}))
    files = {"file": (file_name, file_content, "application/pdf")}

    document_data = sign_client.update_document(
        server_domain=zoho_settings.server_domain,
        access_token=auth_service.get_access_token(),
        document_id=document_id,
        files=files,
    )

    if document_order is not None and document_order < len(sign_doc.documents):
        document_ids = [
            {
                "document_id": document.get("document_id"),
                "document_order": document.get("document_order"),
            }
            for document in document_data.get("document_ids")
        ]

        added_document = document_ids.pop()
        document_ids.insert(document_order, added_document)

        for i, _d in enumerate(document_ids):
            _d["document_order"] = i

        document_data = sign_client.update_document(
            server_domain=zoho_settings.server_domain,
            access_token=auth_service.get_access_token(),
            document_id=document_id,
            document_data={
                "document_ids": document_ids,
            },
        )


def send_document(document_id: str):
    zoho_settings = utils.get_zoho_settings()
    sign_doc = frappe.get_doc("ZohoSign Document", {"document_id": document_id})

    if not sign_doc:
        frappe.throw("ZohoSign Document not found.")
    if not sign_doc.has_permission("write"):
        frappe.throw("You don't have permissions to perform this action.")

    document_data = sign_client.send_document(
        server_domain=zoho_settings.server_domain,
        access_token=auth_service.get_access_token(),
        document_id=document_id,
    )

    return {"document_data": document_data}


def download_document_pdf(
    document_doc: "Document",
    with_certifcate: bool = True,
    merge: bool = False,
    document_password: str | None = None,
):
    zoho_settings = utils.get_zoho_settings()

    pdf_bytes = sign_client.download_document_pdfs(
        server_domain=zoho_settings.server_domain,
        access_token=auth_service.get_access_token(),
        document_id=document_doc.document_id,
        with_coc=with_certifcate,
        merge=merge,
        password=document_password,
    )

    file_docs = utils.create_file_doc_from_bytes(pdf_bytes)

    for idx, file_doc in enumerate(file_docs):
        file_doc.attached_to_doctype = "ZohoSign Document"
        file_doc.attached_to_name = document_doc.name

        if not file_doc.file_name:
            file_doc.file_name = f"{document_doc.documents[idx].document_name}.pdf"
            file_doc.save()
            document_doc.documents[idx].document = file_doc.file_url
            document_doc.documents[idx].document_file = file_doc.name
            continue

        file_doc.save()

        if file_doc.file_name.startswith("completion certificate-"):
            document_doc.certificate = file_doc.file_url
            document_doc.certificate_file = file_doc.name

        else:
            for document in document_doc.documents:
                if document.document_name in file_doc.file_name:
                    document.document = file_doc.file_url
                    document.document_file = file_doc.name
                    break
    return document_doc
