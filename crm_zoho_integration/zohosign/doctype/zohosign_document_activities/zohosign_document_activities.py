# Copyright (c) 2025, OneHash and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZohoSIgnDocumentActivities(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_id: DF.Data
		activity: DF.SmallText | None
		country: DF.Data | None
		ip_address: DF.Data | None
		latitude: DF.Float
		longitude: DF.Float
		operation_type: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		performed_at: DF.Datetime | None
		performed_by: DF.Data | None
		performed_from: DF.Data | None
		signing_order: DF.Int
	# end: auto-generated types
	pass
