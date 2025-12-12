// Copyright (c) 2025, OneHash and contributors
// For license information, please see license.txt

frappe.ui.form.on("Zoho Settings", {
  authorize(frm) {
    if (frm.is_dirty()) {
      frappe.msgprint("Please save the changes before authorizing.");
      return;
    }

    frappe.call({
      method: "crm_zoho_integration.api.auth.get_auth_url",
      freeze: true,
      freeze_message: "Redirecting for authorization...",
      callback: (res) => {
        if (res && res.message) {
          window.location.href = res.message;
        } else {
          frappe.throw("Error occured while requesting for authorization.");
        }
      },
    });
  },

  copy_auth_code(_) {
    frappe.call({
      method: "crm_zoho_integration.api.auth.get_auth_code",
      freeze: true,
      freeze_message: "Getting Auth Code...",
      callback: (res) => {
        if (res && res.message) {
          frappe.utils.copy_to_clipboard(res.message);
        } else {
          frappe.throw("Auth code not found.");
        }
      },
    });
  },

  generate_sign_hmac_secret(frm) {
    frappe.call({
      method: "crm_zoho_integration.api.sign.generate_hmac_secret",
      freeze: true,
      freeze_message: "Generating HMAC Secret Key...",
      callback: (res) => {
        if (res && res.message) {
          frm.set_value("sign_hmac_key", res.message);
        } else {
          frappe.throw("Error occured while generating secret key.");
        }
      },
    });
  },
});
