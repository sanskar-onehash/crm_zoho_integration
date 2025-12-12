import frappe
from crm_zoho_integration import utils
from crm_zoho_integration.integration import meta
from crm_zoho_integration.integration.auth import auth_client
from crm_zoho_integration.integration.sign import sign_meta


def get_auth_url():
    zoho_settings = utils.get_zoho_settings()

    # TODO: Currently, we are integrating only ZohoSign, so hardcoding is OK.
    # In the future, when additional services are added, implement a feature
    # that allows users to select the modules/services they want to enable.
    scopes = []
    for feature in sign_meta.SERVICE_FEATURES:
        scopes.append(
            f"{sign_meta.SERVICE_NAME}.{sign_meta.SERVICE_FEATURES[feature]}.{meta.SCOPE_PERMISSIONS['ALL']}"
        )

    return auth_client.get_auth_url(
        server_domain=zoho_settings.server_domain,
        client_id=zoho_settings.client_id,
        redirect_uri=zoho_settings.redirect_uri,
        scope=",".join(scopes),
    )


def get_redirect_url():
    return utils.get_absolute_url(
        "/api/method/crm_zoho_integration.api.auth.verify_auth"
    )


def get_access_token(ignore_permissions=False):
    zoho_settings = utils.get_zoho_settings()

    access_token = zoho_settings.get_access_token()
    if not access_token:
        access_token = refresh_access_token(ignore_permissions)

    return access_token


def get_auth_code():
    zoho_settings = utils.get_zoho_settings()
    if not (
        zoho_settings.has_permission()
        and zoho_settings.has_permlevel_access_to("authorization_code")
    ):
        frappe.throw("User don't have access to read Authorization Code.")

    if not zoho_settings.authorization_code:
        frappe.throw("Auth code not found.")

    return zoho_settings.get_password("authorization_code")


def generate_access_token(auth_code, location, ignore_permissions=False):
    domain = meta.LOCATIONS_TO_DOMAIN.get(location)
    if not domain:
        frappe.throw(f"Location <strong>{location}</strong> not supported.")

    zoho_settings = utils.get_zoho_settings()
    tokens_data = auth_client.get_tokens(
        server_domain=zoho_settings.server_domain,
        client_id=zoho_settings.client_id,
        client_secret=zoho_settings.get_password("client_secret"),
        auth_code=auth_code,
        redirect_uri=zoho_settings.redirect_uri,
    )
    zoho_settings.update(
        {
            "authorization_code": auth_code,
            "refresh_token": tokens_data.get("refresh_token"),
            "server_domain": domain,
        }
    )
    zoho_settings.set_access_token(
        tokens_data.get("access_token"), tokens_data.get("expires_in")
    )
    zoho_settings.save(ignore_permissions=ignore_permissions)

    return tokens_data.get("access_token")


def refresh_access_token(ignore_permissions=False):
    zoho_settings = utils.get_zoho_settings()

    if not zoho_settings.refresh_token:
        frappe.throw("No refresh token found, please complete the auth flow.")

    token_data = auth_client.refresh_access_token(
        server_domain=zoho_settings.server_domain,
        client_id=zoho_settings.client_id,
        client_secret=zoho_settings.get_password("client_secret"),
        refresh_token=zoho_settings.get_password("refresh_token"),
    )
    zoho_settings.set_access_token(
        token_data.get("access_token"), token_data.get("expires_in")
    )
    zoho_settings.save(ignore_permissions=ignore_permissions)

    return token_data.get("access_token")
