HOST_NAME = "accounts.zoho"

AUTH_VERSION = "v2"
AUTH_BASE_ENDPOINT = f"/oauth/{AUTH_VERSION}"
AUTH_GRANT_TYPES = {
    "AUTHORIZATION_CODE": "authorization_code",
    "REFRESH_TOKEN": "refresh_token",
}
AUTH_GRANT_RESPONSE_TYPE = "code"
AUTH_GRANT_ACCESS_TYPE = "offline"
