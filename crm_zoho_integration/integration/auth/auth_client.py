from crm_zoho_integration.integration import client, utils
from crm_zoho_integration.integration.auth import auth_meta


def get_auth_url(
    server_domain, client_id, redirect_uri, scope, prompt_for_consent=False
):
    params = {
        "access_type": auth_meta.AUTH_GRANT_ACCESS_TYPE,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": auth_meta.AUTH_GRANT_RESPONSE_TYPE,
        "scope": scope,
    }
    if prompt_for_consent:
        params["prompt"] = "consent"

    return f"{utils.get_base_uri(auth_meta.HOST_NAME, server_domain)}{_get_endpoint('auth')}?{utils.prepare_url_params(params)}"


def get_tokens(server_domain, client_id, client_secret, auth_code, redirect_uri):
    token_data = client.post(
        endpoint=_get_endpoint("token"),
        base_uri=utils.get_base_uri(auth_meta.HOST_NAME, server_domain),
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": auth_meta.AUTH_GRANT_TYPES["AUTHORIZATION_CODE"],
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
    )
    return {
        "refresh_token": token_data.get("refresh_token"),
        "access_token": token_data.get("access_token"),
        "expires_in": token_data.get("expires_in"),
    }


def refresh_access_token(server_domain, client_id, client_secret, refresh_token):
    token_data = client.post(
        endpoint=_get_endpoint("token"),
        base_uri=utils.get_base_uri(auth_meta.HOST_NAME, server_domain),
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": auth_meta.AUTH_GRANT_TYPES["REFRESH_TOKEN"],
            "refresh_token": refresh_token,
        },
    )
    return {
        "access_token": token_data.get("access_token"),
        "expires_in": token_data.get("expires_in"),
    }


def _get_endpoint(endpoint):
    return f"{auth_meta.AUTH_BASE_ENDPOINT}/{endpoint}"
