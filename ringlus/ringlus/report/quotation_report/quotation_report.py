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
			"""
	data = frappe.db.sql(query, as_dict=1)

	return columns, data
