# Copyright (c) 2021, jan and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document

class ModularAssembly(Document):
	@frappe.whitelist()
	def delete_modular_component(self, name, qty, old_mc):
		self.delete_raw_material(name,old_mc)
		self.delete_operations(name, old_mc)
	def delete_operations(self, name,old_mc):
		for x in self.operational_cost:

			reference = json.loads(x.reference)
			print("IN OPERATIONAL COST")
			if self.get_index(reference, old_mc, name) or self.get_index(reference, old_mc, name) == 0:
				del reference[self.get_index(reference, old_mc, name)]
			if self.compute_minutes(reference) > 0:
				x.operation_time_in_minutes = self.compute_minutes(reference)
				x.reference = json.dumps(reference)
			else:
				self.get('operational_cost').remove(x)

	def delete_raw_material(self, name,old_mc):
		for i in range(len(self.raw_material) - 1, -1, -1):
			reference = json.loads(self.raw_material[i].reference)
			if self.get_index(reference, old_mc, name) or self.get_index(reference, old_mc, name) == 0:
				del reference[self.get_index(reference, old_mc, name)]
			if len(reference) > 0:

				self.raw_material[i].qty = self.compute_qty(reference)
				self.raw_material[i].reference = json.dumps(reference)
			else:
				self.get('raw_material').remove(self.raw_material[i])

	@frappe.whitelist()
	def get_modular_component(self, name,qty, old_mc):
		mc = frappe.get_doc("Modular Component", name)

		for i in mc.raw_materials:
			if not self.check_items(i,qty,name,old_mc):

				self.append("raw_material",{
					"item_code": i.item_code,
					"qty": i.qty,
					"uom": i.uom,
					"conversion_factor": i.conversion_factor,
					"reference": json.dumps([{
						"item_code": name,
						"qty": i.qty,
						"qty_mc": i.qty
					}])
				})
		for x in mc.operational_cost:
			if not self.check_operational_cost(x,qty,name,old_mc):
				self.append("operational_cost",{
					"workstation": x.workstation,
					"net_hour_rate": x.net_hour_rate,
					"operation": x.operation,
					"operation_time_in_minutes": x.operation_time_in_minutes,
					"reference": json.dumps([{
						"item_code": name,
						"net_hour_rate": x.net_hour_rate,
						"operation_time_in_minutes": x.operation_time_in_minutes,
						"qty": qty
					}]),
				})
		return mc.items
	def check_operational_cost(self, row,qty,name,old_mc):
		for i in self.operational_cost:
			print(i.operation)
			print(row.operation)
			if i.operation == row.operation:
				reference = json.loads(i.reference)
				print(name)
				print(old_mc)
				if name != old_mc:
					del reference[self.get_index(reference, old_mc, name)]
				if not self.existing(reference,name):
					reference.append({
						"item_code": name,
						"net_hour_rate": row.net_hour_rate,
						"operation_time_in_minutes": row.operation_time_in_minutes,
						"qty": qty
					})
				i.operation_time_in_minutes = self.compute_minutes(reference)
				i.reference = json.dumps(reference)

				return True
		return False
	def existing(self, reference,name):
		for i in reference:
			if i['item_code'] == name:
				return True
		return False
	def check_items(self, row,qty,name,old_mc):
		for i in self.raw_material:
			if i.item_code == row.item_code:
				reference = json.loads(i.reference)

				if name != old_mc:
					del reference[self.get_index(reference, old_mc,name)]
				if not self.existing(reference, name):
					reference.append({
						"item_code": name,
						"qty": row.qty,
						"qty_mc": qty
					})
				i.qty = self.compute_qty(reference)
				i.reference = json.dumps(reference)

				return True
		return False

	def compute_qty(self, reference):
		sum = 0
		for i in reference:
			sum += (i['qty'] * i['qty_mc'])
		return sum

	def compute_minutes(self, reference):
		sum = 0
		for i in reference:
			sum += (i['operation_time_in_minutes'] * i['qty'])
		return sum

	def get_index(self, reference, old_mc, name):

		for idx,i in enumerate(reference):
			if i['item_code'] == old_mc:
				self.change_old_item(name)
				return idx
	def change_old_item(self, name):
		for i in self.modular_assembly:
			if i.item_code == name:
				i.old_modular_component = name
				break
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


