from urllib.parse import urlencode


def prepare_url_params(params: dict) -> str:
    return f"?{urlencode(params)}"
