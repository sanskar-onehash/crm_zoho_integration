from urllib.parse import urlencode


def prepare_url_params(params: dict) -> str:
    return f"?{urlencode(params)}"


def get_base_uri(hostname, domain):
    return f"https://{hostname}.{domain}"
