from . import sign_meta
from crm_zoho_integration.integration import client, utils


def fetch_templates(
    server_domain: str,
    access_token: str,
    row_count: int,
    start_index: int,
    sort_order: int | None = None,
):
    templates_data = client.get(
        endpoint=_get_endpoint("/templates"),
        base_uri=utils.get_base_uri(sign_meta.HOST_NAME, server_domain),
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


def _get_endpoint(endpoint):
    return f"{sign_meta.BASE_ENDPOINT}{endpoint}"
