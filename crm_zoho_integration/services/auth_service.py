from crm_zoho_integration import utils
from crm_zoho_integration.integration import meta
from crm_zoho_integration.integration.auth import auth_client
from crm_zoho_integration.integration.sign import sign_client, sign_meta


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

    auth_client.get_auth_url(
        api_base_uri=zoho_settings.api_base_uri,
        client_id=zoho_settings.client_id,
        redirect_uri=zoho_settings.redirect_uri,
        scope=",".join(scopes),
    )


def get_redirect_url():
    return utils.get_absolute_url("/crm_zoho_integration.api.auth.verify_auth")


def get_access_token(ignore_permissions=False):
    zoho_settings = utils.get_zoho_settings()

    access_token = zoho_settings.get_access_token()
    if not access_token:
        access_token = refresh_access_token(ignore_permissions)

    return access_token


def generate_access_token(auth_code, ignore_permissions=False):
    zoho_settings = utils.get_zoho_settings()
    tokens_data = auth_client.get_tokens(
        base_uri=zoho_settings.api_base_uri,
        client_id=zoho_settings.client_id,
        client_secret=zoho_settings.get_password("client_secret"),
        auth_code=auth_code,
        redirect_uri=zoho_settings.redirect_uri,
    )
    zoho_settings.set("refresh_token", tokens_data.get("refresh_token"))
    zoho_settings.set_access_token(
        tokens_data.get("access_token"), tokens_data.get("expires_in")
    )
    zoho_settings.save(ignore_permissions=ignore_permissions)

    return tokens_data.get("access_token")


def refresh_access_token(ignore_permissions=False):
    zoho_settings = utils.get_zoho_settings()

    token_data = auth_client.refresh_access_token(
        base_uri=zoho_settings.api_base_uri,
        client_id=zoho_settings.client_id,
        client_secret=zoho_settings.get_password("client_secret"),
        refresh_token=zoho_settings.get_password("refresh_token"),
    )
    zoho_settings.set_access_token(
        token_data.get("access_token"), token_data.get("expires_in")
    )
    zoho_settings.save(ignore_permissions=ignore_permissions)

    return token_data.get("access_token")
