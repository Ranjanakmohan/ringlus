// Copyright (c) 2016, jan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Quotation Report"] = {
	"filters": [
		{
			"fieldname":"opportunity",
			"label": __("Opportunity"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
                return frappe.db.get_link_options("Opportunity", txt);
            }
		},
		{
			"fieldname":"quotation",
			"label": __("Quotation"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
                return frappe.db.get_link_options("Quotation", txt);
            }
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
		},
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
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "MultiSelectList",
			"reqd": 1,
			get_data: function(txt) {
                return [
                	{value: 'Draft', description: 'Draft'},
					{value: 'Open', description: 'Open'},
					{value: 'Replied', description: 'Replied'},
					{value: 'Ordered', description: 'Ordered'},
					{value: 'Lost', description: 'Lost'},
					{value: 'Cancelled', description: 'Cancelled'},
					{value: 'Expired', description: 'Expired'},
					]
            }
		},
	]
};
