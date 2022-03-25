// Copyright (c) 2022, jan and contributors
// For license information, please see license.txt
var fg_workstation =""
var fg_operation=""
var fg_hour_rate=0
var fg_operation_time=0
var r_rate=0
frappe.ui.form.on('Budget BOM Pro', {
	onload:function(frm){
		frappe.db.get_single_value("Manufacturing Settings","fg_bom_default_workstation")
		.then(d_workstation => {
			fg_workstation = d_workstation
			if(d_workstation){
				frappe.db.get_doc('Workstation', d_workstation)
				.then(doc => {
					fg_hour_rate = doc.hour_rate
				})
			}
		})
		frappe.db.get_single_value("Manufacturing Settings","fg_operation_time_in_minute")
		.then(d_time => {
		fg_operation_time = d_time
		})
		frappe.db.get_single_value("Manufacturing Settings","fg_bom_default_operation")
		.then(d_operation => {
			fg_operation = d_operation
		})
		


		
	},
	sellable_product_category: function () {
		cur_frm.set_query("sellable_product", () => {
			return {
				filters: {
					sellable_product_category: cur_frm.doc.sellable_product_category
				}
			}
		})
	  },
 	 refresh:function(frm){
		frm.set_value("posting_date",frappe.datetime.add_days(frappe.datetime.nowdate()));
  },
  	get_items:function(frm){
		let row=frm.add_child('fg_bom_details',{
			item_code:frm.doc.opportunity + "-" + frm.doc.sellable_product + "-FG",
			item_name:frm.doc.opportunity + "-" + frm.doc.sellable_product + "-FG",
			qty:1,
			uom:"Nos",
			workstation:fg_workstation,
			operation:fg_operation,
			net_hour_rate:fg_hour_rate,
			operation_time_in_minutes:fg_operation_time,
			total_operation_cost: (fg_operation_time / 60) * fg_hour_rate



		})
	frm.refresh_field('fg_bom_details')
	},
	refresh:function(frm){
		cur_frm.set_query("item_code", "raw_materials", (frm, cdt, cdn) => {
            return {
                filters: {
                    item_group: ["!=", "Budget BOM Items"]
                }
            }
        })
		cur_frm.set_query("uoms", "raw_materials", (frm, cdt, cdn) => {
            return {
                filters: {
                    uom_name: ["=", "Nos"]
                }
            }
        })
	},


	
});

frappe.ui.form.on("Budget BOM Raw Material", {
    item_code: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.item_code) {
            frappe.call({
                method: "ringlus.ringlus.doctype.budget_bom_pro.budget_bom_pro.test",
                args: {
                item: d.item_code
        		},
                callback: function (data) {
                    frappe.msgprint( data.message.price_list_rate)
                    frappe.model.set_value(d.doctype, d.name, "rate", data.message);

                },

            });

        }
    }

});

//  frappe.ui.form.on('Budget BOM Raw Material',"item_code",function(frm,cdt,cdn){
//  	let item=locals[cdt][cdn]
//  	if(doc.item_code){
//  		item_price_doc=frappe.get_doc('Item Price',doc.item_code)
//  	}
//  	item.rate=item_price_doc.price_list_rate
//  	frm.refresh_field('raw_materials')

//  });

//r_rate=frappe.model.get_value('Item Price', 'e140908d09', 'price_list_rate')
//  frappe.ui.form.on('Budget BOM Raw Material',{
// 	form_render:function(frm, cdt,cdn){
// 		let item=locals[cdt][cdn]
// 		item.amount=30000
// 		frm.refresh_field('raw_materials')
// 	}
// })





