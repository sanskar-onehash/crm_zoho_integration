import requests
from json import JSONDecodeError


def _prepare_headers(headers=None, access_token=None):
    if headers is None:
        headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = f"Zoho-oauthtoken {access_token}"
    return headers


def get(
    endpoint,
    base_uri,
    access_token=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    throw=True,
):
    headers = _prepare_headers(headers, access_token)

    res = requests.get(
        f"{base_uri}{endpoint}",
        params=params,
        headers=headers,
        data=data,
        json=json,
    )
    if throw:
        res.raise_for_status()

    return _get_response_data(res)


def post(
    endpoint,
    base_uri,
    access_token=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    throw=True,
):
    headers = _prepare_headers(headers, access_token)

    res = requests.post(
        f"{base_uri}{endpoint}",
        headers=headers,
        params=params,
        data=data,
        json=json,
    )
    if throw:
        res.raise_for_status()

    return _get_response_data(res)


def patch(
    endpoint,
    base_uri,
    access_token=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    throw=True,
):
    headers = _prepare_headers(headers, access_token)

    res = requests.patch(
        f"{base_uri}{endpoint}",
        headers=headers,
        params=params,
        data=data,
        json=json,
    )
    if throw:
        res.raise_for_status()

    return _get_response_data(res)


def delete(
    endpoint,
    base_uri,
    access_token=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    throw=True,
):
    headers = _prepare_headers(headers, access_token)

    res = requests.delete(
        f"{base_uri}{endpoint}",
        headers=headers,
        params=params,
        data=data,
        json=json,
    )
    if throw:
        res.raise_for_status()

    return _get_response_data(res)


def _get_response_data(response):
    content_type = response.headers.get("Content-Type", "").lower()
    data = response.text

    if "application/json" in content_type:
        try:
            data = response.json()
        except JSONDecodeError:
            pass
    elif any(
        ct in content_type
        for ct in [
            "image",
            "application/pdf",
            "application/octet-stream",
            "application/zip",
        ]
    ):
        data = response.content

    return data
