# Copyright (c) 2021, jan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ModularAssembly(Document):
	@frappe.whitelist()
	def get_sellable_product(self):
		print(self.opportunity)
		sp = frappe.db.sql(""" SELECT * FROM `tabBudget BOM` WHERE opportunity=%s """, self.opportunity,as_dict=1)
		sps = []
		for i in sp:
			if i.sellable_product not in sps:
				sps.append(i.sellable_product)
		return sps
