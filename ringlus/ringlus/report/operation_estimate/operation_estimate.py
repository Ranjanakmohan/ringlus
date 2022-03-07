# Copyright (c) 2022, jan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
def get_columns():
	"""return columns based on filters"""
	columns = [
		{"label": _("Quotation"),"fieldname": "quotation","fieldtype": "Link","options":"Quotation","width": 200},
		{"label": _("Budget BOM"),"fieldname": "budget_bom","fieldtype": "Link","options":"Budget BOM","width": 320},
		{"label": _("Budget BOM Section Name"), "fieldname": "section_name", "fieldtype": "Data", "width": 400},
		{"label": _("Operation"),"fieldname": "operation","fieldtype": "Link", "options": "Operation","width": 200},
		{"label": _("Operation Time"),"fieldname": "operation_time","fieldtype": "Float","width": 150},
		{"label": _("Net Hour Rate"),"fieldname": "net_hour_rate","fieldtype": "Float","width": 200},
		{"label": _("Operation Cost"),"fieldname": "operation_cost","fieldtype": "Currency","width": 150},
	]


	return columns
def execute(filters=None):
	columns, data = get_columns(), []
	condition = get_conditions(filters)
	query = """ SELECT 
 					Q.name as quotation, 
					BBR.budget_bom, 
					BBR.budget_bom, 
					BBD.operation, 
					SUM(BBD.net_hour_rate) as net_hour_rate, 
					SUM(BBD.operation_time_in_minutes) as operation_time, 
					SUM(BB.total_operation_cost) as operation_cost,
					BBD.parentfield
				FROM `tabQuotation` Q 
 				INNER JOIN `tabBudget BOM References` BBR ON BBR.parent = Q.name
 				INNER JOIN `tabBudget BOM` BB ON BB.name = BBR.budget_bom
 				INNER JOIN `tabBudget BOM Details` BBD ON BBD.parent = BB.name
 				{0} GROUP BY BB.name,BBD.operation
 				
			""".format(condition)
	data = frappe.db.sql(query, as_dict=1)
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
	return columns,data


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
		conditions += " BB.name= '{0}' ".format(filters.get("budget_bom"))

	return conditions