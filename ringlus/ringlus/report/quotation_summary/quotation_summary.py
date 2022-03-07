# Copyright (c) 2022, jan and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_columns():
	"""return columns based on filters"""
	columns = [
		{"label": _("Budget BOM"),"fieldname": "budget_bom","fieldtype": "Link","options":"Budget BOM","width": 320},
		{"label": _("RFQ Sl No"),"fieldname": "rfq_sl_no","fieldtype":"Data","width": 250},
		{"label": _("Product Description"),"fieldname": "product_description","fieldtype": "Data","width": 200},
		{"label": _("Qty"),"fieldname": "qty","fieldtype": "Float","width": 120},
		{"label": _("Rate"),"fieldname": "rate","fieldtype": "Currency","width": 150},
		{"label": _("Amount"),"fieldname": "amount","fieldtype": "Currency","width": 150},
		{"label": _("Material Overhead %"),"fieldname": "material_overhead","fieldtype": "Float","width": 200},
		{"label": _("Operation Overhead %"),"fieldname": "operation_overhead","fieldtype": "Float","width": 200},
		{"label": _("Material Margin %"),"fieldname": "material_margin","fieldtype": "Float","width": 200},
		{"label": _("Operation Margin %"),"fieldname": "operation_margin","fieldtype": "Float","width": 200},
	]
	return columns
def get_conditions(filters):
	conditions = ""

	if filters.get("customer"):
		conditions += "WHERE"
		conditions += " Q.customer = '{0}' ".format(filters.get("customer"))

	if filters.get("quotation"):
		if conditions:
			conditions += " and "
		else:
			conditions += " WHERE "
		conditions += " Q.name= '{0}' ".format(filters.get("quotation"))

	return conditions
def execute(filters=None):
	columns, data = get_columns(), []
	condition = get_conditions(filters)

	data = frappe.db.sql(""" 
						SELECT Q.name,
								QI.qty, 
								QI.item_code,
							 QI.rate, 
							 QI.amount, 
							 QI.material_overhead, 
							 QI.operation_overhead, 
							 QI.material_margin, 
							 QI.operation_margin FROM `tabQuotation` Q 
					  	INNER JOIN `tabQuotation Item` QI ON QI.parent = Q.name {0}
						""".format(condition),as_dict=1)

	for i in data:
		print(i.name)
		bb = frappe.db.sql(""" SELECT * FROM `tabBudget BOM References` WHERE parent=%s """, i.name,as_dict=1)
		for x in bb:
			bbr = frappe.db.sql(""" SELECT * FROM `tabBudget BOM` BB 
									INNER JOIN `tabBudget BOM Details` BBD ON BBD.parent = BB.name 
									WHERE BB.name = %s and BBD.item_code=%s""", (x.budget_bom,i.item_code),as_dict=1)
			if len(bbr) > 0:
				i.budget_bom = x.budget_bom
				i.rfq_si_no = bbr[0].rfq_si_no
				i.product_description = bbr[0].product_description
	return columns, data
