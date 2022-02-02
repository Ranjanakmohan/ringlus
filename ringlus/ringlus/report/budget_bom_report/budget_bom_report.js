// Copyright (c) 2016, jan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Budget BOM Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
						"reqd": 1,

		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
						"reqd": 1,


		},
		{
			"fieldname":"product_category",
			"label": __("Product Category"),
			"fieldtype": "Link",
			"options": "Sellable Product Category",
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
		},
		{
			"fieldname":"customer_name",
			"label": __("Customer Name"),
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			"fieldname":"based_on",
			"label": __("Based On"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": ['Material','Operation'],
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
                return [
                	{value: 'Pending', description: 'Pending'},
					{value: 'To Quotation', description: 'To Quotation'},
					{value: 'To Design', description: 'To Design'},
					{value: 'Updated Changes', description: 'Updated Changes'},
					{value: 'To Material Request', description: 'To Material Request'},
					{value: 'Quotation In Progress', description: 'Quotation In Progress'},
					{value: 'To PO and SO', description: 'To PO and SO'},
					{value: 'To PO', description: 'To PO'},
					{value: 'To SO', description: 'To SO'},
					{value: 'Completed', description: 'Completed'},
					{value: 'To BOM', description: 'To BOM'},
					{value: 'To Purchase Receipt', description: 'To Purchase Receipt'},
					{value: 'To Work Order', description: 'To Work Order'},
					{value: 'To Deliver and Bill', description: 'To Deliver and Bill'},
					]
            }
		},
	]
};
