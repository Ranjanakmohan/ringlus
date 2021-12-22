# Copyright (c) 2021, jan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ModularComponent(Document):
	def autoname(self):
		self.name = self.items[0].item_name

	def validate(self):
		for i in self.raw_materials:
			if i.uom:
				i.conversion_factor = self.get_conversion_factor(i.item_code, i.uom)

	@frappe.whitelist()
	def get_conversion_factor(self, item_code, uoms):
		uom = frappe.db.sql(""" SELECT * FROm `tabUOM Conversion Detail` WHERE parent=%s and uom=%s""",
							(item_code, uoms), as_dict=1)

		if len(uom) > 0:
			return uom[0].conversion_factor

		return 1

