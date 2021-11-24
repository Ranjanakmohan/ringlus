frappe.ui.form.on("Additional Salary", {
    fetch_attendance_requests: function () {
        if(cur_frm.doc.employee && (cur_frm.doc.from_date && cur_frm.doc.to_date || cur_frm.doc.payroll_date)){
           frappe.call({
               method: "amsecc.doc_events.additional_salary.get_attendance_requests",
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