import frappe

@frappe.whitelist()
def validate_as(doc, method):
    for i in doc.additional_request:
        frappe.db.sql(""" UPDATE `tabAttendance Request` SET additional_salary=%s WHERE name=%s """, (doc.name, i.attendance_request))
        frappe.db.commit()
@frappe.whitelist()
def get_attendance_requests(employee, from_date, to_date, is_recurring, payroll_date):

    query = """ SELECT * FROm `tabAttendance Request` WHERE docstatus=1 and employee='{0}' and (additional_salary is null or additional_salary='')""".format(employee)
    attendance_request = frappe.db.sql(query, as_dict=1)
    ar = []
    for i in attendance_request:
        ar.append({
            "from_date": i.from_date,
            "to_date": i.to_date,
            "base": i.base,
            "overtime_hour": i.overtime_hour,
            "overtime_amount": i.overtime_amount,
            "attendance_request": i.name
        })

    return ar


@frappe.whitelist()
def get_salary_structure(employee, total_working_hours):
    ss = frappe.db.sql(""" SELECT * FROM `tabSalary Structure Assignment` WHERE employee=%s ORDER BY from_date DESC LIMIT 1""", (employee), as_dict=1)

    total = 0
    if len(ss) > 0:
        total = float((ss[0].base / 30 / 8) * 1.5) * float(total_working_hours)
    return total