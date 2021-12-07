// Copyright (c) 2021, jan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Modular Assembly', {
	refresh: function(frm) {
        cur_frm.set_query("opportunity", () => {
	        return {
	            filters:{
	                status: 'Open'
                }
            }
        })

         cur_frm.fields_dict.modular_assembly.grid.get_field("item_code").get_query =
                function() {
            var names = Array.from(cur_frm.doc.modular_assembly, x => "item_code" in x ? x.item_code:"")
                    var filters =  [
                        ["name", "not in", names]
                    ]
                    return {
                         filters: filters
                    }
                }
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
frappe.ui.form.on('Modular Assembly Details', {
	item_code: function(frm, cdt, cdn) {
       var d = locals[cdt][cdn]
		if(d.item_code){
       		frappe.db.get_doc("Modular Component", d.item_code)
				.then(doc => {

            if(cur_frm.doc.operational_cost.length > 0 && !cur_frm.doc.operational_cost[0].workstation && !cur_frm.doc.operational_cost[0].operation){
                cur_frm.clear_table("operational_cost")
                cur_frm.refresh_field("operational_cost")
            }
            if(cur_frm.doc.raw_material.length > 0 && !cur_frm.doc.raw_material[0].item_code){
                cur_frm.clear_table("raw_material")
                cur_frm.refresh_field("raw_material")
            }
                for(var xy=0;xy<doc.items.length;xy+=1){
                        d.uom = doc.items[0].uom
                        d.remarks= doc.items[0].item_description
                        cur_frm.refresh_field("modular_assembly")
                    }
					for(var x=0;x<doc.operational_cost.length;x+=1){
						if(!check_operational_cost(doc.operational_cost[x], cur_frm, d)) {
                            cur_frm.add_child("operational_cost", {
                                workstation: doc.operational_cost[x].workstation,
                                net_hour_rate: doc.operational_cost[x].net_hour_rate,
                                operation: doc.operational_cost[x].operation,
                                operation_time_in_minutes: doc.operational_cost[x].operation_time_in_minutes,
                                reference: JSON.stringify([{
                                    item_code: d.item_code,
                                    net_hour_rate: doc.operational_cost[x].net_hour_rate,
                                    operation_time_in_minutes: doc.operational_cost[x].operation_time_in_minutes}]),
                            })

                            cur_frm.refresh_field('operational_cost')

                        }
                    }
					for(var i=0;i<doc.raw_materials.length;i+=1){
						if(!check_items(doc.raw_materials[i], cur_frm, d)) {
							cur_frm.add_child("raw_material", {
								item_code: doc.raw_materials[i].item_code,
								qty: doc.raw_materials[i].qty,
								uom: doc.raw_materials[i].uom,
								conversion_factor: doc.raw_materials[i].conversion_factor,
								reference: JSON.stringify([{
                                item_code: d.item_code,
                                qty: doc.raw_materials[i].qty}]),
							})
							cur_frm.refresh_field('raw_material')
						}
					}
			})
		}
	},
	before_modular_assembly_remove: function (frm, cdt, cdn) {
	    console.log("naa man")
        var d = locals[cdt][cdn]
	    remove_row(cur_frm, d, 'raw_material')
	    remove_row(cur_frm, d, 'operational_cost')
    }
});

function remove_row(cur_frm, dd, table_name) {
    if(cur_frm.doc[table_name]) {
        for (var x = cur_frm.doc[table_name].length - 1; x >= 0; x -= 1) {
            if (cur_frm.doc[table_name][x].reference.includes(dd.item_code)) {
                var spliced_row = false
                var splice_index = 0
                var spliced = 0
                var reference = JSON.parse(cur_frm.doc[table_name][x].reference)
                for(var xx=0;xx<reference.length;xx+=1){
                    console.log("NET HOUR RATE")
                    console.log(reference[xx]['item_code'])
                    console.log(reference[xx]['net_hour_rate'])
                    console.log(dd.item_code)
                    if(reference[xx]['item_code'] === dd.item_code && table_name === 'operational_cost'){
                        console.log("OPERATIONAL COST")
                        cur_frm.doc[table_name][x].net_hour_rate -= reference[xx]['net_hour_rate']
                        cur_frm.doc[table_name][x].operation_time_in_minutes -= reference[xx]['operation_time_in_minutes']
                        spliced = xx
                         if(cur_frm.doc[table_name][x].net_hour_rate === 0 && cur_frm.doc[table_name][x].operation_time_in_minutes === 0){
                            spliced_row = true
                            splice_index = x
                        }
                    } else if(reference[xx]['item_code'] === dd.item_code && table_name === 'raw_material'){
                        console.log("RAW MATERIAL")
                        cur_frm.doc[table_name][x].qty -= reference[xx]['qty']
                        if(cur_frm.doc[table_name][x].qty === 0){
                            spliced_row = true
                            splice_index = x
                        }
                        spliced = xx
                    }

                }
                reference.splice(spliced, 1);
                cur_frm.doc[table_name][x].reference = JSON.stringify(reference)
                if(spliced_row){
                    cur_frm.doc[table_name].splice(x, 1);
                    spliced_row = false
                }
                cur_frm.refresh_field(table_name)
            }
        }
    }
}
function check_items(item, cur_frm, d) {
	if(cur_frm.doc.raw_material){
		 for(var x=0;x<cur_frm.doc.raw_material.length;x+=1){
            var item_row = cur_frm.doc.raw_material[x]
            if(item_row.item_code === item.item_code){
                var reference = JSON.parse(item_row.reference)
                reference.push({
                    item_code: d.item_code,
                    qty: item.qty
                })
                console.log(reference)
                item_row.qty += item.qty
                item_row.reference = JSON.stringify(reference)
                cur_frm.refresh_field("raw_material")
                return true
            }
        }
        return false
	}

}
function check_operational_cost(operational_cost, cur_frm,d) {
	if(cur_frm.doc.operational_cost){
		 for(var x=0;x<cur_frm.doc.operational_cost.length;x+=1){
            var item_row = cur_frm.doc.operational_cost[x]
            if(item_row.workstation === operational_cost.workstation && item_row.operation === operational_cost.operation){
                 var reference = JSON.parse(item_row.reference)
                reference.push({
                    item_code: d.item_code,
                    net_hour_rate: operational_cost.net_hour_rate,
                    operation_time_in_minutes: operational_cost.operation_time_in_minutes
                })
                console.log(reference)
                item_row.net_hour_rate += operational_cost.net_hour_rate
                item_row.operation_time_in_minutes += operational_cost.operation_time_in_minutes
                item_row.reference = JSON.stringify(reference)
                cur_frm.refresh_field("operational_cost")
                return true
            }
        }
        return false
	}

}