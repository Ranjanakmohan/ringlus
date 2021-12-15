// Copyright (c) 2021, jan and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOM Item Template', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('BOM Item Template Details', {
	uom: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn]

        if(d.uom){
            frappe.call({
                method: "ringlus.ringlus.doctype.budget_bom.budget_bom.get_conversion_factor",
                args: {
                    item_code: d.item_code,
                    uoms: d.uom
                },
                async: false,
                callback: function (r) {
                    d.uom_conversion_factor = r.message
                }
            })
        }
    }
});
