frappe.ui.form.on("Attendance Request", {
    from_date: function () {
        cur_frm.doc.to_date = cur_frm.doc.from_date
        refresh_field("to_date")
    },
    employee: function () {
        if(cur_frm.doc.employee){
            frappe.call({
            method: "ringlus.doc_events.attendance_request.get_ss",
            args:{
                employee: cur_frm.doc.employee
            },
            callback: function (r) {
                cur_frm.doc.salary_structure = r.message[0]
                cur_frm.doc.base = r.message[1]
                cur_frm.refresh_fields(["salary_structure", "base"])
            }
            })
        }

    },
      overtime_hour: function () {
       cur_frm.doc.overtime_amount =cur_frm.doc.overtime_hour * cur_frm.doc.overtime_multiplication_factor * (cur_frm.doc.base / (30 * 8))
      cur_frm.refresh_field("overtime_amount")

    }
})