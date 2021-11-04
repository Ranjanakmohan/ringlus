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
	}
});

frappe.ui.form.on('Modular Assembly Details', {
	item_code: function(frm, cdt, cdn) {
       var d = locals[cdt][cdn]
		if(d.item_code){
       		frappe.db.get_doc("Modular Component", d.item_code)
				.then(doc => {
					console.log(doc)
					for(var x=0;x<doc.operational_cost.length;x+=1){
							cur_frm.add_child("operational_cost", {
								workstation_1: doc.operational_cost[x].workstation_1,
								workstation_2: doc.operational_cost[x].workstation_2,
								workstation_3: doc.operational_cost[x].workstation_3,
								workstation_4: doc.operational_cost[x].workstation_4,
								workstation_5: doc.operational_cost[x].workstation_5,
								net_hour_rate_1: doc.operational_cost[x].net_hour_rate_1,
								net_hour_rate_2: doc.operational_cost[x].net_hour_rate_2,
								net_hour_rate_3: doc.operational_cost[x].net_hour_rate_3,
								net_hour_rate_4: doc.operational_cost[x].net_hour_rate_4,
								net_hour_rate_5: doc.operational_cost[x].net_hour_rate_5,
								operation_1: doc.operational_cost[x].operation_1,
								operation_2: doc.operational_cost[x].operation_2,
								operation_3: doc.operational_cost[x].operation_3,
								operation_4: doc.operational_cost[x].operation_4,
								operation_5: doc.operational_cost[x].operation_5,
								operation_time_in_minutes_1: doc.operational_cost[x].operation_time_in_minutes_1,
								operation_time_in_minutes_2: doc.operational_cost[x].operation_time_in_minutes_2,
								operation_time_in_minutes_3: doc.operational_cost[x].operation_time_in_minutes_3,
								operation_time_in_minutes_4: doc.operational_cost[x].operation_time_in_minutes_4,
								operation_time_in_minutes_5: doc.operational_cost[x].operation_time_in_minutes_5
							})

							cur_frm.refresh_field('operational_cost')

					}
					for(var i=0;i<doc.raw_materials.length;i+=1){
						if(!check_items(doc.raw_materials[i], cur_frm)) {
							cur_frm.add_child("raw_material", {
								item_code: doc.raw_materials[i].item_code,
								qty: doc.raw_materials[i].qty,
							})
							cur_frm.refresh_field('raw_material')
						}
					}
			})
		}
	}
});

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