// Copyright (c) 2025, OneHash and contributors
// For license information, please see license.txt

frappe.ui.form.on("Zoho Settings", {
  authorize(frm) {
    if (frm.is_dirty()) {
      frappe.msgprint("Please save the changes before providing the consent.");
      return;
    }

    frappe.call({
      method: "crm_zoho_integration.api.auth.get_auth_url",
      freeze: true,
      freeze_message: "Redirecting for authorization...",
      callback: ({ message: url }) => url && (window.location.href = url),
    });
  },
});
