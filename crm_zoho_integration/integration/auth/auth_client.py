from crm_zoho_integration.integration import base_client as base
from crm_zoho_integration.integration import utils


AUTH_VERSION = "v2"
AUTH_BASE_ENDPOINT = f"/oauth/{AUTH_VERSION}"
AUTH_GRANT_TYPES = {
    "AUTHORIZATION_CODE": "authorization_code",
    "REFRESH_TOKEN": "refresh_token",
}
AUTH_GRANT_RESPONSE_TYPE = "code"
AUTH_GRANT_ACCESS_TYPE = "offline"


def get_auth_url(
    api_base_uri, client_id, redirect_uri, scope, prompt_for_consent=False
):
    params = {
        "access_type": AUTH_GRANT_ACCESS_TYPE,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": AUTH_GRANT_RESPONSE_TYPE,
        "scope": scope,
    }
    if prompt_for_consent:
        params["prompt"] = "consent"

    return f"{api_base_uri}{_get_endpoint('auth')}?{utils.prepare_url_params(params)}"


def get_tokens(base_uri, client_id, client_secret, auth_code, redirect_uri):
    token_data = base.post(
        endpoint=_get_endpoint("token"),
        base_uri=base_uri,
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": AUTH_GRANT_TYPES["AUTHORIZATION_CODE"],
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
    )
    return {
        "refresh_token": token_data.get("refresh_token"),
        "access_token": token_data.get("access_token"),
        "expires_in": token_data.get("expires_in"),
    }


def refresh_access_token(base_uri, client_id, client_secret, refresh_token):
    token_data = base.post(
        endpoint=_get_endpoint("token"),
        base_uri=base_uri,
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": AUTH_GRANT_TYPES["REFRESH_TOKEN"],
            "refresh_token": refresh_token,
        },
    )
    return {
        "access_token": token_data.get("access_token"),
        "expires_in": token_data.get("expires_in"),
    }


def _get_endpoint(endpoint):
    return f"{AUTH_BASE_ENDPOINT}/{endpoint}"
