# Copyright (c) 2022, jan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
def get_columns():
	"""return columns based on filters"""
	columns = [
		{"label": _("Quotation"),"fieldname": "quotation","fieldtype": "Link","options":"Quotation","width": 200},
		{"label": _("Budget BOM"),"fieldname": "budget_bom","fieldtype": "Link","options":"Budget BOM","width": 320},
		{"label": _("Budget BOM Section Name"),"fieldname": "section_name","fieldtype":"Data","width": 400},
		{"label": _("Item Code"),"fieldname": "item_code","fieldtype": "Link", "options": "Item","width": 200},
		{"label": _("Make"),"fieldname": "make","fieldtype": "Data","width": 200},
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
  										BBRM.discount_rate as rate,
  										BBRM.amount,
  										BBRM.idx,
  										BBRM.parentfield,
  										I.default_item_manufacturer as make
									FROM `tabQuotation` Q 
									INNER JOIN `tabBudget BOM References` BBR ON BBR.parent = Q.name
									INNER JOIN `tabBudget BOM` BB ON BB.name = BBR.budget_bom
									INNER JOIN `tabBudget BOM Raw Material` BBRM ON BBRM.parent = BB.name
									INNER JOIN `tabItem` I ON I.name = BBRM.item_code  {0}
								""".format(condition), as_dict=1)
	print(data)
	for i in data:
		if i.parentfield in ["electrical_bom_details","electrical_bom_raw_material"]:
			i.section_name = "Electrical BOM"
		elif i.parentfield in ["fg_bom_details"]:
			i.section_name = "FG BOM"
		elif i.parentfield in ["mechanical_bom_details","mechanical_bom_raw_material"]:
			i.section_name = "Mechanical BOM"
		elif i.parentfield in ["fg_sellable_bom_details","fg_sellable_bom_raw_material"]:
			i.section_name = "Enclosure"

	if filters.get("section_name"):
		data = [i for i in data if i.section_name == filters.get("section_name")]

	if filters.get("item_code"):
		data.append({
			"item_code":"TOTALS",
			"estimate_qty": get_sum(data, 'estimate_qty'),
			"stock_qty": get_sum(data, 'stock_qty'),
			"rate": get_sum(data, 'rate'),
			"amount": get_sum(data, 'amount'),
		})
	return columns, data
def get_sum(data, field):
	total = 0
	for i in data:
		total += i[field]
	return total
def get_conditions(filters):
	conditions = ""

	if filters.get("customer"):
		conditions += "WHERE"
		conditions += " BB.customer = '{0}' ".format(filters.get("customer"))
	if filters.get("make"):
		conditions += "WHERE"
		conditions += " I.default_item_manufacturer = '{0}' ".format(filters.get("make"))

	if filters.get("item_category"):
		conditions += "WHERE"
		conditions += " I.item_category = '{0}' ".format(filters.get("item_category"))

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