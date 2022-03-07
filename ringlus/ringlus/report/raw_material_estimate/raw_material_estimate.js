// Copyright (c) 2022, jan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Raw Material Estimate"] = {
	"filters": [
{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"quotation",
			"label": __("Quotation"),
			"fieldtype": "Link",
			"options": "Quotation"
		},
		{
			"fieldname":"budget_bom",
			"label": __("Budget BOM"),
			"fieldtype": "Link",
			"options": "Budget BOM"
		},
		{
			"fieldname":"section_name",
			"label": __("Section Name"),
			"fieldtype": "Select",
			"options": "FG BOM\nElectrical BOM\nMechanical BOM\nEnclosure"
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		},
		{
			"fieldname":"item_category",
			"label": __("Item Category"),
			"fieldtype": "Link",
			"options": "Item Category"
		},
		{
			"fieldname":"make",
			"label": __("Make"),
			"fieldtype": "Data",
		},
	]
};
