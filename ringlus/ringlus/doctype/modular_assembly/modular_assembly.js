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
					console.log(doc)
					for(var x=0;x<doc.operational_cost.length;x+=1){
						if(!check_operational_cost(doc.operational_cost[x], cur_frm)) {
                            cur_frm.add_child("operational_cost", {
                                workstation: doc.operational_cost[x].workstation,
                                net_hour_rate: doc.operational_cost[x].net_hour_rate,
                                operation: doc.operational_cost[x].operation,
                                operation_time_in_minutes: doc.operational_cost[x].operation_time_in_minutes,
                                reference: d.item_code,
                            })

                            cur_frm.refresh_field('operational_cost')

                        }
                    }
					for(var i=0;i<doc.raw_materials.length;i+=1){
						if(!check_items(doc.raw_materials[i], cur_frm)) {
							cur_frm.add_child("raw_material", {
								item_code: doc.raw_materials[i].item_code,
								qty: doc.raw_materials[i].qty,
								uom: doc.raw_materials[i].uom,
								reference: d.item_code,
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

function remove_row(cur_frm, d, table_name) {
    if(cur_frm.doc[table_name]) {
        for (var x = cur_frm.doc[table_name].length - 1; x >= 0; x -= 1) {
            if (cur_frm.doc[table_name][x].reference === d.item_code) {
                console.log("SPLIICE")
                cur_frm.doc[table_name].splice(x, 1);
                cur_frm.refresh_field(table_name)
            }
        }
    }
}
function check_items(item, cur_frm) {
	if(cur_frm.doc.raw_material){
		 for(var x=0;x<cur_frm.doc.raw_material.length;x+=1){
            var item_row = cur_frm.doc.raw_material[x]
            if(item_row.item_code === item.item_code){
                item_row.qty += item.qty
                cur_frm.refresh_field("raw_material")
                return true
            }
        }
        return false
	}

}
function check_operational_cost(operational_cost, cur_frm) {
	if(cur_frm.doc.operational_cost){
		var existing = false
		 for(var x=0;x<cur_frm.doc.operational_cost.length;x+=1){
            var item_row = cur_frm.doc.operational_cost[x]
            if(item_row.workstation === operational_cost.workstation){
                item_row.net_hour_rate += operational_cost.net_hour_rate
                cur_frm.refresh_field("operational_cost")
                existing = true
            }
            if(item_row.operation === operational_cost.operation){
                item_row.operation_time_in_minutes += operational_cost.operation_time_in_minutes
                cur_frm.refresh_field("operational_cost")
                existing = true
            }
        }
        return existing
	}

}