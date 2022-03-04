# Copyright (c) 2022, jan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
def get_columns():
	"""return columns based on filters"""
	columns = [
		{"label": _("Quotation"),"fieldname": "quotation","fieldtype": "Link","options":"Quotation","width": 200},
		{"label": _("Budget BOM"),"fieldname": "budget_bom","fieldtype": "Link","options":"Budget BOM","width": 320},
		{"label": _("Item Code"),"fieldname": "item_code","fieldtype": "Link", "options": "Item","width": 200},
		{"label": _("Estimate Qty"),"fieldname": "estimate_qty","fieldtype": "Float","width": 150},
		{"label": _("Estimate UOM"),"fieldname": "estimated_uom","fieldtype": "Data","width": 200},
		{"label": _("UOM Conversion Factor"),"fieldname": "uom_conversion_factor","fieldtype": "Float","width": 200},
		{"label": _("Stock Qty"),"fieldname": "stock_qty","fieldtype": "Float","width": 150},
		{"label": _("Stock UOM"),"fieldname": "stock_uom","fieldtype": "Link","options": "UOM","width": 150},
		{"label": _("Item Group"),"fieldname": "item_group","fieldtype": "Link","options": "Item Group","width": 150},
		{"label": _("Item Category"),"fieldname": "item_category","fieldtype": "Link","options": "Item Category","width": 150},
		{"label": _("Estimate Rate"),"fieldname": "rate","fieldtype": "Currency","width": 150},

		{"label": _("Amount"),"fieldname": "amount","fieldtype": "Currency","width": 150},
	]


	return columns
def execute(filters=None):
	columns, data =  get_columns(), []
	condition = get_conditions(filters)

	data = frappe.db.sql(""" SELECT
  										Q.name as quotation,
  										BB.name as budget_bom,
  										BBRM.item_code,
  										BBRM.qty as estimate_qty,
  										BBRM.uoms as estimated_uom,
  										BBRM.uom_conversion_factor,
  										BBRM.stock_qty,
  										BBRM.stock_uom,
  										BBRM.item_group,
  										I.item_category,
  										BBRM.rate,
  										BBRM.amount,
  										BBRM.idx,
  										BBRM.parentfield
  										
  										
									FROM `tabQuotation` Q 
									INNER JOIN `tabBudget BOM References` BBR ON BBR.parent = Q.name
									INNER JOIN `tabBudget BOM` BB ON BB.name = BBR.budget_bom
									INNER JOIN `tabBudget BOM Raw Material` BBRM ON BBRM.parent = BB.name
									INNER JOIN `tabItem` I ON I.name = BBRM.item_code  {0}
								""".format(condition), as_dict=1)
	print(data)
	return columns, data

def get_conditions(filters):
	conditions = ""

	if filters.get("customer"):
		conditions += "WHERE"
		conditions += " BB.customer = '{0}' ".format(filters.get("customer"))

	if filters.get("quotation"):
		if conditions:
			conditions += " and "
		else:
			conditions += "WHERE"
		conditions += " Q.name = '{0}' ".format(filters.get("quotation"))

	if filters.get("budget_bom"):
		if conditions:
			conditions += " and "
		else:
			conditions += "WHERE"
		conditions += " BB.name = '{0}' ".format(filters.get("budget_bom"))

	if filters.get("item_code"):
		if conditions:
			conditions += " and "
		else:
			conditions += "WHERE"
		conditions += " BBRM.item_code = '{0}' ".format(filters.get("item_code"))

	if filters.get("item_group"):
		if conditions:
			conditions += " and "
		else:
			conditions += "WHERE"
		conditions += "  BBRM.item_group = '{0}' ".format(filters.get("item_group"))


	return conditions