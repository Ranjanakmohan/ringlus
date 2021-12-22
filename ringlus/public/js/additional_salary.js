frappe.ui.form.on("Additional Salary", {
    fetch_attendance_requests: function () {
        if(cur_frm.doc.employee && (cur_frm.doc.from_date && cur_frm.doc.to_date || cur_frm.doc.payroll_date)){
           frappe.call({
               method: "ringlus.doc_events.additional_salary.get_attendance_requests",
               args: {
                   employee: cur_frm.doc.employee,
                   from_date: cur_frm.doc.from_date ? cur_frm.doc.from_date : "",
                   to_date: cur_frm.doc.from_date ? cur_frm.doc.to_date : "",
                   is_recurring: cur_frm.doc.is_recurring,
                   payroll_date: cur_frm.doc.payroll_date ?  cur_frm.doc.payroll_date : ""
               },
               callback: function (r) {
                   var total_amount = 0
                   for(var x=0;x < r.message.length;x+=1){
                       total_amount += r.message[x].overtime_amount
                       cur_frm.add_child("additional_request",r.message[x])
                       cur_frm.refresh_field("additional_request")
                   }
                   cur_frm.doc.amount = total_amount
                   cur_frm.refresh_field("amount")
               }
           })
        }
    }
})



cur_frm.cscript.salary_component = function () {
    if(cur_frm.doc.salary_component){
        frappe.db.get_doc('Salary Component', cur_frm.doc.salary_component)
            .then(sc => {
                cur_frm.doc.is_hour_based = sc.is_hour_based
                cur_frm.refresh_field("is_hour_based")
                cur_frm.set_df_property("amount", "reqd", !cur_frm.doc.is_hour_based)
                cur_frm.set_df_property("amount", "read_only", cur_frm.doc.is_hour_based)
                cur_frm.set_df_property("total_working_hour", "hidden", !cur_frm.doc.is_hour_based)
                 compute_total_working_hrs(cur_frm)
            })
    }
}
cur_frm.cscript.total_working_hour = function () {
    compute_total_working_hrs(cur_frm)
}
function compute_total_working_hrs(cur_frm) {

    if(cur_frm.doc.is_hour_based && cur_frm.doc.employee && cur_frm.doc.total_working_hour > 0){
        console.log("NAA MAAAAN")
        frappe.call({
            method: "ringlus.doc_events.additional_salary.get_salary_structure",
            args: {
                employee: cur_frm.doc.employee,
                total_working_hours: cur_frm.doc.total_working_hour ? cur_frm.doc.total_working_hour : 0
            },
            callback: function (r) {
                console.log("MESSAGE")
                console.log(r.message)
                    cur_frm.doc.amount = r.message
                    cur_frm.refresh_field("amount")

            }
        })
    } else {
        cur_frm.doc.amount = 0
        cur_frm.doc.total_working_hour = 0
        cur_frm.refresh_field("amount")
        cur_frm.refresh_field("total_working_hour")

    }


}