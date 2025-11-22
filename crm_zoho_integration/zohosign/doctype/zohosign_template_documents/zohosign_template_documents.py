# Copyright (c) 2025, OneHash and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ZohoSignTemplateDocuments(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		document_id: DF.Data
		document_name: DF.Data | None
		document_order: DF.Int
		document_size: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		total_pages: DF.Int
	# end: auto-generated types
	pass
