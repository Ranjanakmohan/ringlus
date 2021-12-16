// Copyright (c) 2021, jan and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOM Item Template', {
	update_custom_fields: function(frm) {
            frappe.call({
                method: "ringlus.doc_events.utils.create_custom_fields",
                args: {},
                freeze: true,
                freeze_message: "Updating Custom Fields",
                async: false,
                callback: function (r) {
                    frappe.msgprint("Done Updating")
                }
            })
	},
    refresh: function () {
        cur_frm.set_query("uom", "items", (frm, cdt, cdn) => {

                var d = locals[cdt][cdn]
                var uoms = []
                cur_frm.call({
                    doc: cur_frm.doc,
                    method: 'get_uom',
                    args: {
                        item_code: d.item_code ? d.item_code : ""
                    },
                    freeze: true,
                    freeze_message: "Get UOM...",
                    async:false,
                    callback: (r) => {
                        uoms = r.message

                    }
                })
                return {
                                filters:{
                                    name: ["in",uoms]
                                }
                            }

        })
    }
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
                    d.conversion_factor = r.message
                    cur_frm.refresh_field(d.parentfield)
                }
            })
        }
    }
});
