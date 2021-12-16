# Copyright (c) 2021, jan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BOMItemTemplate(Document):
	@frappe.whitelist()
	def get_uom(self, item_code):
		uom = frappe.db.sql(""" SELECT * FROM `tabUOM Conversion Detail` WHERE parent=%s""", item_code, as_dict=1)
		data = [i.uom for i in uom]
		print(data)
		return data
