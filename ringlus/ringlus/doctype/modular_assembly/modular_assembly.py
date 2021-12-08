# Copyright (c) 2021, jan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ModularAssembly(Document):
	@frappe.whitelist()
	def autoname(self):
		count = frappe.db.sql(""" SELECT COUNT(*) as count FROM `tabModular Assembly`""", as_dict=1)
		names = self.opportunity + "-" + self.sellable_product + "-" + str((count[0].count if count[0].count else 1) + 1 )
		print(names)
		existing = frappe.db.sql(""" SELECT * FROM `tabModular Assembly` WHERE name=%s """, names)
		print("naaaaaaaaaame")
		print(self.opportunity + "-" + self.sellable_product + "-" + str((count[0].count if count[0].count else 1) + 1 ))
		print(existing)
		self.name = names if len(existing) == 0 else self.opportunity + "-" + self.sellable_product + "-" + str((count[0].count if count[0].count else 1) + 2 )
	@frappe.whitelist()
	def get_sellable_product(self):
		print(self.opportunity)
		sp = frappe.db.sql(""" SELECT * FROM `tabBudget BOM` WHERE opportunity=%s """, self.opportunity,as_dict=1)
		sps = []
		for i in sp:
			if i.sellable_product not in sps:
				sps.append(i.sellable_product)
		return sps
