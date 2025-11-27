// Copyright (c) 2025, OneHash and contributors
// For license information, please see license.txt

frappe.ui.form.on("ZohoSign Template", {
  refresh(frm) {
    addZohoSignTemplateActions(frm);
  },
});

function addZohoSignTemplateActions(frm) {
  if (!frm.is_new()) {
    addUseTemplateButton(frm);
  }
}

function addUseTemplateButton(frm) {
  const BTN_LABEL = "Use Template";

  frm.page.remove_inner_button(BTN_LABEL);
  frm.page.add_inner_button(
    BTN_LABEL,
    async () => {
      const dialog = new frappe.ui.Dialog({
        title: BTN_LABEL,
        fields: [
          {
            label: "Document Name",
            fieldname: "document_name",
            fieldtype: "Data",
            reqd: 1,
          },
          {
            label: "Actions",
            fieldname: "actions",
            fieldtype: "Table",
            options: "ZohoSign Document Actions",
            fields: getActionFieldsForUse(),
            data: frm.doc.actions.map((action) => {
              const preparedAction = { ...action };
              delete preparedAction.name;
              return preparedAction;
            }),
          },
          {
            label: "Notes",
            fieldname: "notes",
            fieldtype: "Small Text",
          },
        ],
        size: "large",
        primary_action_label: BTN_LABEL,
        primary_action: (values) => {
          frappe.call({
            method: "crm_zoho_integration.api.sign.use_template",
            args: {
              template_id: frm.doc.name,
              template_data: {
                ...values,
              },
            },
            freeze: true,
            freeze_message: "Creating ZohoSign Document...",
            callback: (res) => {
              if (res.message && !res.exc) {
                dialog.hide();
                frappe.show_alert({
                  indicator: "green",
                  message: "ZohoSign document created and sent successfully.",
                });
              }
            },
          });
        },
      });
      dialog.show();
    },
    null,
    "primary",
  );
}

function getActionFieldsForUse() {
  const fieldOverrides = {
    action_type: { reqd: 1, read_only: 1 },
    recipient_name: { reqd: 1 },
    recipient_email: { reqd: 1 },
    signing_order: { read_only: 1 },
    role: { read_only: 1 },
    action_status: { hidden: 1 },
  };
  return frappe.get_meta("ZohoSign Document Actions").fields.map((field) => ({
    ...field,
    ...(fieldOverrides[field.fieldname] || []),
  }));
}
