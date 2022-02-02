# Copyright (c) 2013, jan and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_columns(filters):
	if filters.get("based_on") == 'Material':
		return [
			{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
			{"label": _("Raw Material Item Code"), "fieldname": "item_code", "fieldtype": "Data", "width": 200},
			{"label": _("Estimate Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 200},
			{"label": _("Estimate UOM"), "fieldname": "uoms", "fieldtype": "Data","width": 150},
			{"label": _("Discounted Rate"), "fieldname": "discount_rate", "fieldtype": "Currency","width": 200},
			{"label": _("Discount Percentage"), "fieldname": "discount_percentage", "fieldtype": "Float", "width": 150},
			{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 150},
		]
	else:
		return [
			{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
			{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
			{"label": _("Operation Time in Minutes"), "fieldname": "operation_time_in_minutes", "fieldtype": "Float", "width": 200},
			{"label": _("Net Hour Rate"), "fieldname": "net_hour_rate", "fieldtype": "Float", "width": 150},
			{"label": _("Total Operation Cost"), "fieldname": "total_operation_cost", "fieldtype": "Currency", "width": 200},
		]
def get_conditions(filters):
	conditions = " and BB.posting_date BETWEEN '{0}' and '{1}' ".format(filters.get("from_date"),filters.get("to_date"))

	if filters.get("product_category"):
		conditions += " and BB.sellable_produce_category = '{0}' ".format(filters.get("product_category"))

	if filters.get("item_group") and filters.get("based_on") == "Material":
		conditions += " and BBRM.item_group = '{0}' ".format(filters.get("item_group"))

	if filters.get("customer_name"):
		conditions += " and BB.customer = '{0}' ".format(filters.get("customer_name"))

	if len(filters.get("status")) == 1:
		conditions += " and BB.status='{0}'".format(filters.get("status")[0])
	elif len(filters.get("status")) > 1:
		conditions += " and BB.status in {0} ".format(tuple(filters.get("status")))
	return conditions
def execute(filters=None):
	columns, data = get_columns(filters), []

	conditions = get_conditions(filters)
	if filters.get("based_on") == "Material":
		data = get_material_query(conditions)
	if filters.get("based_on") == "Operation":
		data = get_operation_query(conditions)
	return columns, data


def get_material_query(conditions):

	return frappe.db.sql(""" SELECT BB.posting_date,BBRM.item_code,BBRM.qty,BBRM.uoms,BBRM.discount_rate,BBRM.discount_percentage,BBRM.amount FROM `tabBudget BOM` BB 
 				INNER JOIN `tabBudget BOM Raw Material` BBRM ON BBRM.parent = BB.name 
 				WHERE BB.docstatus=1 {0}
			""".format(conditions), as_dict=1)

def get_operation_query(conditions):

	bom_details = frappe.db.sql(""" SELECT 
								BB.posting_date,
								BBRM.item_name,
								BBRM.operation_time_in_minutes,
								BBRM.net_hour_rate,
								BBRM.total_operation_cost
 						FROM `tabBudget BOM` BB 
						INNER JOIN `tabBudget BOM Details` BBRM ON BBRM.parent = BB.name 
						WHERE BB.docstatus=1 {0}
			""".format(conditions), as_dict=1)

	# bom_fg_details = frappe.db.sql(""" SELECT
	# 								BB.posting_date,
	# 								BBRM.item_name,
	#  						FROM `tabBudget BOM` BB
	# 						INNER JOIN `tabBudget BOM FG Details` BBRM ON BBRM.parent = BB.name
	# 						WHERE BB.docstatus=1 {0}
	# 			""".format(conditions), as_dict=1)

	return bom_details