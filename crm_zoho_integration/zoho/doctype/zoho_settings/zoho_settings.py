# Copyright (c) 2025, OneHash and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


TOKEN_EXPIRY_BUFFER = 5 * 60  # In Seconds; 5 mins


class ZohoSettings(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        access_token: DF.Password | None
        access_token_expiry: DF.Datetime | None
        authorization_code: DF.Password | None
        client_id: DF.Data | None
        client_secret: DF.Password | None
        development_mode: DF.Check
        enabled: DF.Check
        redirect_uri: DF.Data | None
        refresh_token: DF.Password | None
        server_domain: DF.Data | None
        sign_hmac_key: DF.Password | None
        sign_webhook_url: DF.Data | None
    # end: auto-generated types

    @property
    def redirect_uri(self):
        from crm_zoho_integration.services.auth_service import get_redirect_url

        return get_redirect_url()

    @property
    def sign_webhook_url(self):
        from crm_zoho_integration.services.sign_service import get_sign_webhook_url

        return get_sign_webhook_url()

    def get_access_token(self):
        cur_time = frappe.utils.get_datetime()
        access_token = None

        if self.access_token:
            if self.development_mode:
                access_token = self.get_password("access_token")
            else:
                token_expiry = frappe.utils.get_datetime(self.access_token_expiry)
                if (token_expiry - cur_time).total_seconds() > TOKEN_EXPIRY_BUFFER:
                    access_token = self.get_password("access_token")

        return access_token

    def set_access_token(self, access_token: str, expires_in: int):
        cur_time = frappe.utils.get_datetime()
        expiry_time = frappe.utils.add_to_date(
            cur_time, seconds=expires_in, as_datetime=True
        )
        self.update({"access_token": access_token, "access_token_expiry": expiry_time})
