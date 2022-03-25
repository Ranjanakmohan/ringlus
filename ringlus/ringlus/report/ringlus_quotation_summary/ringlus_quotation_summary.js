// Copyright (c) 2022, jan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ringlus Quotation Summary"] = {
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
		}
	]
};
