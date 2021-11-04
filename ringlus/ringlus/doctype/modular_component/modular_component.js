// Copyright (c) 2021, jan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Modular Component', {
	refresh: function(frm) {
cur_frm.get_field("items").grid.cannot_add_rows = true;
cur_frm.refresh_field("items")
	}
});
