# Copyright (c) 2025, OneHash and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZohoSignTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from crm_zoho_integration.zohosign.doctype.zohosign_document_actions.zohosign_document_actions import ZohoSignDocumentActions
		from crm_zoho_integration.zohosign.doctype.zohosign_template_documents.zohosign_template_documents import ZohoSignTemplateDocuments
		from frappe.types import DF

		actions: DF.Table[ZohoSignDocumentActions]
		description: DF.LongText | None
		documents: DF.Table[ZohoSignTemplateDocuments]
		email_reminders: DF.Check
		expiration_days: DF.Int
		is_deleted: DF.Check
		is_sequential: DF.Check
		naming_series: DF.Literal["ZH-SIGN-TMPL-"]
		notes: DF.TextEditor | None
		owner_email: DF.Data | None
		owner_first_name: DF.Data | None
		owner_id: DF.Data | None
		owner_last_name: DF.Data | None
		reminder_period: DF.Int
		request_type_id: DF.Data | None
		request_type_name: DF.Data | None
		template_created_on: DF.Datetime | None
		template_id: DF.Data | None
		template_modified_on: DF.Datetime | None
		template_name: DF.Data | None
	# end: auto-generated types
	pass
