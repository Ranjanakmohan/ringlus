frappe.ui.form.on('Quotation Item', {
    estimated_bom_material_cost: function(frm) {
        compute_margin_operations(cur_frm)
    },
    estimated_bom_operation_cost: function(frm) {
        compute_margin_operations(cur_frm)
    },
    material_margin: function(frm) {
        compute_margin_operations(cur_frm)
    },
    operation_margin: function(frm) {
        compute_margin_operations(cur_frm)
    },
    material_overhead: function(frm) {
        compute_margin_operations(cur_frm)
    },
    operation_overhead: function(frm) {
        compute_margin_operations(cur_frm)
    },
    items_add: function (frm, cdt, cdn) {
        var item_row = locals[cdt][cdn]
        item_row.material_overhead = cur_frm.doc.default_material_overhead
        item_row.operation_overhead = cur_frm.doc.default_operation_overhead
        item_row.material_margin = cur_frm.doc.default_material_margin
        item_row.operation_margin = cur_frm.doc.default_operation_margin
    }
})
function update_items(item, cur_frm) {
        for(var x=0;x<cur_frm.doc.items.length;x+=1){
            var item_row = cur_frm.doc.items[x]
            if(item_row.item_code === item.item_code){
                item_row.estimated_bom_material_cost  = item.total_raw_material_cost
                item_row.estimated_bom_operation_cost  = item.total_operation_cost + item.total_additional_operational_cost

                item_row.material_overhead_amount = item_row.estimated_bom_material_cost * (item_row.material_overhead / 100 )
                item_row.material_cost = item_row.estimated_bom_material_cost + (item_row.estimated_bom_material_cost * (item_row.material_overhead / 100 ))

                item_row.operation_overhead_amount = item_row.estimated_bom_operation_cost * (item_row.operation_overhead / 100 )
                item_row.operation_cost = item_row.estimated_bom_operation_cost + (item_row.estimated_bom_operation_cost * (item_row.operation_overhead / 100 ))

                item_row.material_margin_amount = (item_row.material_cost / (1 - (item_row.material_margin / 100 ))) - item_row.material_cost
                item_row.total_margin_cost = item_row.material_cost + item_row.material_margin_amount
                item_row.operation_margin_amount = (item_row.operation_cost / (1 - (item_row.operation_margin / 100 ))) - item_row.operation_cost
                item_row.total_operation_cost = item_row.operation_cost + item_row.operation_margin_amount

                item_row.total_cost = item_row.total_margin_cost + item_row.total_operation_cost
                item_row.rate = item_row.total_cost
                item_row.base_rate = item_row.total_cost
                item_row.net_rate = item_row.total_cost
                item_row.base_net_rate = item_row.total_cost
                item_row.amount = item_row.rate * item_row.qty
                item_row.base_amount = item_row.amount
                item_row.net_amount = item_row.amount
                item_row.base_net_amount = item_row.amount

                cur_frm.refresh_field("items")

            }
        }
        compute_total(cur_frm)
}
function compute_total(cur_frm) {
    var total = 0
    $.each(cur_frm.doc.items || [], function(i, items) {
        total += items.amount
    });
    cur_frm.doc.total = total
    cur_frm.doc.grand_total = total - cur_frm.doc.discount_amount
    cur_frm.doc.rounded_total =  cur_frm.doc.grand_total
    cur_frm.refresh_fields(["total",'grand_total','rounded_total'])
}
frappe.ui.form.on('Quotation', {
    apply_default: function (frm, cdt, cdn) {
        frappe.confirm('Are you sure you want to apply default?',
        () => {
             compute_margin_operations(cur_frm, true)
        }, () => {})

    },
	default_material_overhead: function(frm, cdt, cdn) {
        compute_margin_operations(cur_frm)
    },
    default_operation_overhead: function(frm, cdt, cdn) {
        compute_margin_operations(cur_frm)
    },
    default_material_margin: function(frm, cdt, cdn) {
        compute_margin_operations(cur_frm)
    },
    default_operation_margin: function(frm, cdt, cdn) {
        compute_margin_operations(cur_frm)
    },
    update_cost: function(frm) {
	    cur_frm.clear_table("payment_schedule")
	    cur_frm.refresh_field("payment_schedule")
	    frappe.call({
            method: "ringlus.doc_events.quotation.get_updated_costs",
            args: {
                budget_boms: cur_frm.doc.budget_bom_reference ? cur_frm.doc.budget_bom_reference : []
            },
            async: false,
            callback: function (r) {
                console.log(r.message)
                for(var x=0;x<r.message.length;x+=1){
                    update_items(r.message[0][x], cur_frm)
                }
            }
        })
    },
	refresh: function(frm) {
         document.querySelectorAll("[data-fieldname='apply_default']")[1].style.backgroundColor ="blue"
       document.querySelectorAll("[data-fieldname='apply_default']")[1].style.color ="white"
       document.querySelectorAll("[data-fieldname='apply_default']")[1].style.fontWeight ="bold"
        cur_frm.fields_dict["items"].grid.add_custom_button(__('Update Cost'),
			function() {
             frappe.confirm('Are you sure you want to update cost?',
                () => {
                    cur_frm.trigger("update_cost")
                }, () => {})

        }).css('background-color','#00008B').css('color','white').css('margin-left','10px').css('margin-right','10px').css('font-weight','bold')

        cur_frm.add_custom_button(__('Opportunity with Budget BOM'),
				function() {
                    var query_args = {
                        query:"ringlus.doc_events.quotation.get_opportunity",
                        filters: {}
                    }
					 var d = new frappe.ui.form.MultiSelectDialog({
                            doctype: "Opportunity",
                            target: cur_frm,
                            setters: [
                                {
                                    label: "Customer",
                                    fieldname: "party_name",
                                    fieldtype: "Link",
                                    options: "Customer",
                                    default: cur_frm.doc.party_name || undefined
                                }
                            ],
                            add_filters_group: 0,
                            date_field: "posting_date",
                            get_query() {
                                return query_args
                            },
                            action(selections) {
                                fetch_boms(cur_frm, selections)
                                d.dialog.hide()
                            }
                        });
				}, __("Get Items From"), "btn-default");
    }
})

function fetch_boms(cur_frm, selections) {
    for(var x=0;x<selections.length;x+=1){
        var check_opp = check_opportunity(selections[x])
        if(!check_opp){
            cur_frm.add_child("budget_bom_opportunity",{
                opportunity: selections[x]
            })
            cur_frm.refresh_field("budget_bom_opportunity")

            frappe.db.get_list('Budget BOM', {
                filters: {
                   opportunity: selections[x],
                    status: 'To Quotation',
                    docstatus: 1
                }
            }).then(records => {
                         if(cur_frm.doc.items && !cur_frm.doc.items[0].item_code){
                                cur_frm.clear_table("items")
                                cur_frm.refresh_field("items")
                            }
                for(var xx=0;xx<records.length;xx+=1){
                    frappe.db.get_doc('Budget BOM', records[xx].name)
                        .then(doc => {
                            cur_frm.doc.party_name = doc.customer
                            cur_frm.doc.customer_name = doc.customer_name
                            cur_frm.doc.additional_operating_cost += doc.total_additional_operational_cost
                            cur_frm.refresh_fields(["party_name","additional_operating_cost", "customer_name"])
                            cur_frm.add_child("budget_bom_reference",{
                                budget_bom: doc.name
                            })
                            cur_frm.refresh_field("budget_bom_reference")

                        for(var ii=0;ii<doc.fg_bom_details.length;ii+=1){
                                var material_cost = doc.total_raw_material_cost + (doc.total_raw_material_cost * (cur_frm.doc.default_material_overhead / 100 ))
                                var operation_cost = doc.total_operation_cost + (doc.total_operation_cost *(cur_frm.doc.default_operation_overhead / 100 ))
                                  cur_frm.add_child("items",{
                                        "description": doc.fg_bom_details[ii].item_name + "<br>RFQ Si No - " + doc.fg_bom_details[ii].rfq_si_no + "<br>" + "Product Description - " + doc.fg_bom_details[ii].product_description,
                                        "item_code": doc.fg_bom_details[ii].item_code,
                                        "item_name": doc.fg_bom_details[ii].item_name,
                                        "qty": doc.fg_bom_details[ii].qty,
                                        "uom": doc.fg_bom_details[ii].uom,
                                        "amount": doc.total_cost * doc.fg_bom_details[ii].qty,

                                        "estimated_bom_material_cost": doc.total_raw_material_cost,
                                        "material_overhead": cur_frm.doc.default_material_overhead,
                                        "material_overhead_amount": doc.total_raw_material_cost * (cur_frm.doc.default_material_overhead / 100 ),
                                        "material_cost": material_cost,

                                        "estimated_bom_operation_cost": doc.total_operation_cost + doc.total_additional_operational_cost,
                                        "operation_overhead": cur_frm.doc.default_operation_overhead,
                                        "operation_overhead_amount": doc.total_operation_cost * (cur_frm.doc.default_operation_overhead / 100 ),
                                        "operation_cost": operation_cost,

                                        "material_margin": cur_frm.doc.default_material_margin,
                                        "material_margin_amount":  (material_cost / (1 - (cur_frm.doc.default_material_margin / 100 ))) - material_cost,
                                        "total_margin_cost": material_cost + ((material_cost / (1 - (cur_frm.doc.default_material_margin / 100 ))) - material_cost),

                                        "operation_margin": cur_frm.doc.default_operation_margin,
                                        "operation_margin_amount": (operation_cost /  (1 - (cur_frm.doc.default_operation_margin / 100 ))) - operation_cost,
                                        "total_operation_cost": operation_cost + ((operation_cost /  (1 - (cur_frm.doc.default_operation_margin / 100 ))) - operation_cost),

                                        "total_cost": (material_cost + ((material_cost / (1 - (cur_frm.doc.default_material_margin / 100 ))) - material_cost)) + (operation_cost + ((operation_cost /  (1 - (cur_frm.doc.default_operation_margin / 100 ))) - operation_cost)),
                                        "rate": (material_cost + ((material_cost / (1 - (cur_frm.doc.default_material_margin / 100 ))) - material_cost)) + (operation_cost + ((operation_cost /  (1 - (cur_frm.doc.default_operation_margin / 100 ))) - operation_cost))
                                    })
                                    cur_frm.refresh_field("items")



                    }
                        })
                    }
            })
        }



    }
}
function check_items(item, cur_frm) {
        for(var x=0;x<cur_frm.doc.items.length;x+=1){
            var item_row = cur_frm.doc.items[x]
            if(item_row.item_code === item.item_code){
                item_row.qty += item.qty
                cur_frm.refresh_field("items")
                return true
            }
        }
        return false
}
function check_opportunity(name) {
    console.log("NAAAAAAAAAME")
    console.log(name)
    if(cur_frm.doc.budget_bom_opportunity){
        console.log("WAAAAAAAAT")
        for(var x=0;x<cur_frm.doc.budget_bom_opportunity.length;x+=1){
            var item_row = cur_frm.doc.budget_bom_opportunity[x]
            console.log(item_row.opportunity)
            console.log(name)
            if(item_row.opportunity === name){
                console.log("AFTER CHECK")
                return true
            }
        }
    }

        return false
}
function compute_margin_operations(cur_frm, apply = false) {
    if(cur_frm.doc.items){
        for(var x=0;x<cur_frm.doc.items.length;x+=1){
            var item_row = cur_frm.doc.items[x]
            item_row.material_overhead = item_row.material_overhead === 0 || apply ? cur_frm.doc.default_material_overhead : item_row.material_overhead
            item_row.operation_overhead = item_row.operation_overhead === 0 || apply ?  cur_frm.doc.default_operation_overhead : item_row.operation_overhead
            item_row.material_margin = item_row.material_margin === 0 || apply ?  cur_frm.doc.default_material_margin : item_row.material_margin
            item_row.operation_margin = item_row.operation_margin === 0 || apply ?  cur_frm.doc.default_operation_margin : item_row.operation_margin

            item_row.material_overhead_amount = item_row.estimated_bom_material_cost * (item_row.material_overhead / 100 )
            item_row.material_cost = item_row.estimated_bom_material_cost + (item_row.estimated_bom_material_cost * (item_row.material_overhead / 100 ))

            item_row.operation_overhead_amount = item_row.estimated_bom_operation_cost * (item_row.operation_overhead / 100 )
            item_row.operation_cost = item_row.estimated_bom_operation_cost + (item_row.estimated_bom_operation_cost * (item_row.operation_overhead / 100 ))

            item_row.material_margin_amount = (item_row.material_cost / (1 - (item_row.material_margin / 100 ))) - item_row.material_cost
            item_row.total_margin_cost = item_row.material_cost + item_row.material_margin_amount


            item_row.operation_margin_amount = (item_row.operation_cost / (1 - (item_row.operation_margin/ 100 ))) - item_row.operation_cost
            item_row.total_operation_cost = item_row.operation_cost + item_row.operation_margin_amount

            item_row.total_cost = item_row.total_margin_cost + item_row.total_operation_cost

            item_row.rate = item_row.total_cost
            item_row.base_rate = item_row.total_cost
            item_row.net_rate = item_row.total_cost
            item_row.base_net_rate = item_row.total_cost
            item_row.amount = item_row.rate * item_row.qty
            item_row.base_amount = item_row.amount
            item_row.net_amount = item_row.amount
            item_row.base_net_amount = item_row.amount
            cur_frm.refresh_field("items")

        }
    }

}
