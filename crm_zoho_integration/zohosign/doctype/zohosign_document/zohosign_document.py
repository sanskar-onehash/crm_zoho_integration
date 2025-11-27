# Copyright (c) 2025, OneHash and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZohoSignDocument(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from crm_zoho_integration.zohosign.doctype.zohosign_document_actions.zohosign_document_actions import ZohoSignDocumentActions
		from crm_zoho_integration.zohosign.doctype.zohosign_template_documents.zohosign_template_documents import ZohoSignTemplateDocuments
		from frappe.types import DF

		action_time: DF.Datetime | None
		actions: DF.Table[ZohoSignDocumentActions]
		amended_from: DF.Link | None
		description: DF.SmallText | None
		document_created_on: DF.Datetime | None
		document_expires_by: DF.Datetime | None
		document_id: DF.Data
		document_modified_on: DF.Datetime | None
		document_name: DF.Data | None
		documents: DF.Table[ZohoSignTemplateDocuments]
		expiration_days: DF.Int
		from_template: DF.Link
		in_process: DF.Check
		is_deleted: DF.Check
		is_expiring: DF.Check
		is_sequential: DF.Check
		naming_series: DF.Literal["", "ZH-SIGN-DOC-"]
		notes: DF.SmallText | None
		owner_email: DF.Data | None
		owner_first_name: DF.Data | None
		owner_id: DF.Data | None
		owner_last_name: DF.Data | None
		request_status: DF.Data | None
		request_type_id: DF.Data | None
		request_type_name: DF.Data | None
		self_sign: DF.Check
		sign_percentage: DF.Percent
		sign_submitted_on: DF.Datetime | None
	# end: auto-generated types
	pass
