// Copyright (c) 2021, jan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Modular Component', {
	refresh: function(frm) {
		cur_frm.get_field("items").grid.cannot_add_rows = true;
		cur_frm.refresh_field("items")


	}
});
frappe.ui.form.on('Modular Assembly Raw Material', {
    item_code: function (frm, cdt,cdn) {
        var d = locals[cdt][cdn]
        if(d.item_code){
            frappe.db.get_doc("Item", d.item_code)
                .then(doc => {
                    d.uom = doc.stock_uom
                        cur_frm.refresh_field("raw_material")
            })
        }
    }
})