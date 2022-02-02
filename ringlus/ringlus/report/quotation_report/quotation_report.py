# Copyright (c) 2013, jan and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def get_columns():
	columns = [
		{"label": _("Date"), "fieldname": "transaction_date", "fieldtype": "Date", "width": 150},
		{"label": _("Customer Name"), "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
		{"label": _("RFQ SI No"), "fieldname": "rfq_si_no", "fieldtype": "Date", "width": 200},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data","width": 150},
		{"label": _("Product Description"), "fieldname": "product_description", "fieldtype": "Data","width": 200},
		{"label": _("Budget BOM Name"), "fieldname": "budget_bom", "fieldtype": "Data", "width": 150},
		{"label": _("Estimated BOM Material Cost"), "fieldname": "estimated_bom_material_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Material Overhead %"), "fieldname": "material_overhead", "fieldtype": "Float", "width": 150},
		{"label": _("Material Overhead Amount"), "fieldname": "material_overhead_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Material Cost"), "fieldname": "material_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Material Margin %"), "fieldname": "material_margin", "fieldtype": "Float", "width": 150},
		{"label": _("Material Margin Amount"), "fieldname": "material_margin_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Total Margin Cost"), "fieldname": "total_margin_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Total Cost"), "fieldname": "total_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Estimated BOM Operation Cost"), "fieldname": "estimated_bom_operation_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Operation Overhead %"), "fieldname": "operation_overhead", "fieldtype": "Float", "width": 150},
		{"label": _("Operation Overhead Amount"), "fieldname": "operation_overhead_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Operation Cost"), "fieldname": "operation_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Operation Margin %"), "fieldname": "operation_margin", "fieldtype": "Float", "width": 150},
		{"label": _("Operation Margin Amount"), "fieldname": "operation_margin_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Total Operation Cost"), "fieldname": "total_operation_cost", "fieldtype": "Currency", "width": 150},
		{"label": _("Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 150},
		{"label": _("Rate"), "fieldname": "rate", "fieldtype": "Currency", "width": 150},
		{"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 150},
	]
	return columns
def execute(filters=None):
	columns, data = get_columns(), []
	conditions = get_condition(filters)
	o_conditions = get_o_conditions(filters,conditions)
	query = """ SELECT 
 					Q.transaction_date,
 					Q.customer_name,
 					QI.*,
 					BBF.rfq_si_no,
 					BBF.product_description,
 					BBR.budget_bom
				FROM `tabQuotation` Q 
 				INNER JOIN `tabBudget BOM References` BBR ON BBR.parent = Q.name 
 				INNER JOIN `tabBudget BOM Details` BBF ON BBF.parent = BBR.budget_bom 
 				INNER JOIN `tabQuotation Item` QI ON QI.parent = Q.name and QI.item_code = BBF.item_code
 				{0}
 				WHERE Q.docstatus = 1 {1}
			""".format(o_conditions,conditions)
	print("==========================================")
	print(query)
	data = frappe.db.sql(query, as_dict=1)

	return columns, data

def get_o_conditions(filters,conditions):
	condition = ""
	if len(filters.get("opportunity")) == 1:
		condition += " INNER JOIN `tabOpportunities` O ON O.parent = Q.name "
		conditions += " and O.opportunity = '{0}'".format(filters.get("opportunity")[0])
	elif len(filters.get("quotation")) > 1:
		condition += " INNER JOIN `tabOpportunities` O ON O.parent = Q.name "
		conditions += " and O.opportunity in {0}".format(tuple(filters.get("opportunity")))

	return condition
def get_condition(filters):
	condition = " and Q.transaction_date BETWEEN '{0}' and '{1}' ".format(filters.get("from_date"),filters.get("to_date"))
	if len(filters.get("status")) == 1:
		condition += " and Q.status='{0}'".format(filters.get("status")[0])
	elif len(filters.get("status")) > 1:
		for i in filters.get("status"):
			condition += " and Q.status in {0} ".format(tuple(filters.get("status")))

	if filters.get("customer"):
		condition += " and Q.customer = '{0}'".format(filters.get("customer"))


	if len(filters.get("quotation")) == 1:
		condition += " and Q.name='{0}'".format(filters.get("quotation")[0])
	elif len(filters.get("quotation")) > 1:
		for i in filters.get("quotation"):
			condition += " and Q.name in {0} ".format(tuple(filters.get("quotation")))


	return condition