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
					for(var x=0;x<doc.items.length;x+=1){
						if(doc.items[x].item_name === d.item_code) {
							d.workstation_1 = doc.items[x].workstation_1
							d.workstation_2 = doc.items[x].workstation_2
							d.workstation_3 = doc.items[x].workstation_3
							d.workstation_4 = doc.items[x].workstation_4
							d.workstation_5 = doc.items[x].workstation_5
							d.net_hour_rate_1 = doc.items[x].net_hour_rate_1
							d.net_hour_rate_2 = doc.items[x].net_hour_rate_2
							d.net_hour_rate_3 = doc.items[x].net_hour_rate_3
							d.net_hour_rate_4 = doc.items[x].net_hour_rate_4
							d.net_hour_rate_5 = doc.items[x].net_hour_rate_5
							d.operation_1 = doc.items[x].operation_1
							d.operation_2 = doc.items[x].operation_2
							d.operation_3 = doc.items[x].operation_3
							d.operation_4 = doc.items[x].operation_4
							d.operation_5 = doc.items[x].operation_5
							d.operation_time_in_minutes_1 = doc.items[x].operation_time_in_minutes_1
							d.operation_time_in_minutes_2 = doc.items[x].operation_time_in_minutes_2
							d.operation_time_in_minutes_3 = doc.items[x].operation_time_in_minutes_3
							d.operation_time_in_minutes_4 = doc.items[x].operation_time_in_minutes_4
							d.operation_time_in_minutes_5 = doc.items[x].operation_time_in_minutes_5
														cur_frm.refresh_field('modular_assembly')

						}
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