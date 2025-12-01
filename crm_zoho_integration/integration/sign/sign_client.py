import frappe
from . import sign_meta
from crm_zoho_integration.integration import client, utils


def get_template(template_id: str, access_token: str, server_domain: str) -> dict:
    template_data = client.get(
        endpoint=_get_endpoint(f"/templates/{template_id}"),
        base_uri=_get_base_uri(server_domain),
        access_token=access_token,
    )

    return template_data.get("templates")


def fetch_templates(
    server_domain: str,
    access_token: str,
    row_count: int,
    start_index: int,
    sort_order: int | None = None,
) -> dict:
    templates_data = client.get(
        endpoint=_get_endpoint("/templates"),
        base_uri=_get_base_uri(server_domain),
        access_token=access_token,
        data={
            "row_count": row_count,
            "start_index": start_index,
            "sort_column": sign_meta.TEMPLATES_SORT_COLUMN,
            "sort_order": sort_order or sign_meta.TEMPLATES_SORT_ORDER,
        },
    )
    page_context = templates_data.get("page_context") or {}
    return {
        "templates": templates_data.get("templates"),
        "has_more_rows": page_context.get("has_more_rows"),
        "total_count": page_context.get("total_count"),
    }


def use_template(
    template_id: str,
    template_payload: dict,
    quick_send: bool,
    access_token: str,
    server_domain: str,
) -> dict:
    document_data = client.post(
        endpoint=_get_endpoint(f"/templates/{template_id}/createdocument"),
        base_uri=_get_base_uri(server_domain),
        access_token=access_token,
        data=frappe.utils.urlencode(
            {
                "data": {"templates": template_payload},
                "is_quicksend": quick_send,
            }
        ),
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    return document_data.get("requests")


def download_document_pdfs(
    server_domain: str,
    access_token: str,
    document_id: str,
    with_coc: bool = True,
    merge: bool = False,
    password: str | None = None,
):
    return client.get(
        endpoint=_get_endpoint(f"/requests/{document_id}/pdf"),
        base_uri=_get_base_uri(server_domain),
        access_token=access_token,
        params={"with_coc": with_coc, "merge": merge, "password": password},
    )


def _get_base_uri(server_domain):
    return utils.get_base_uri(sign_meta.HOST_NAME, server_domain)


def _get_endpoint(endpoint):
    return f"{sign_meta.BASE_ENDPOINT}{endpoint}"
