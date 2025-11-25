# Copyright (c) 2025, OneHash and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZohoSignDocumentActions(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_id: DF.Data | None
		action_status: DF.Data | None
		action_type: DF.Link
		allow_signing: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		private_notes: DF.LongText | None
		recipient_email: DF.Data | None
		recipient_name: DF.Data | None
		recipient_phone_number: DF.Phone | None
		role: DF.Int
		signing_order: DF.Int
		verification_type: DF.Data | None
		verify_recipient: DF.Check
	# end: auto-generated types
	pass
