# Copyright (c) 2021, jan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ModularComponent(Document):
	def autoname(self):
		self.name = self.items[0].item_name
