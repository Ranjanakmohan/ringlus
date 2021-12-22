import frappe

@frappe.whitelist()
def get_attendance_requests(employee, from_date, to_date, is_recurring, payroll_date):
    condition = ""
    if is_recurring:
        condition += " and from_date='{0}' and to_date='{1}'".format(from_date, to_date)
    else:
        condition += " and '{0}' BETWEEN from_date and to_date".format(payroll_date)

    query = """ SELECT * FROm `tabAttendance Request` WHERE docstatus=1 and employee='{0}' {1}""".format(employee, condition)
    print(query)
    attendance_request = frappe.db.sql(query, as_dict=1)
    ar = []
    for i in attendance_request:
        ar.append({
            "from_date": i.from_date,
            "to_date": i.to_date,
            "base": i.base,
            "overtime_hour": i.overtime_hour,
            "overtime_amount": i.overtime_amount,
        })

    return ar


@frappe.whitelist()
def get_salary_structure(employee, total_working_hours):
    ss = frappe.db.sql(""" SELECT * FROM `tabSalary Structure Assignment` WHERE employee=%s ORDER BY from_date DESC LIMIT 1""", (employee), as_dict=1)

    total = 0
    if len(ss) > 0:
        total = float((ss[0].base / 30 / 8) * 1.5) * float(total_working_hours)
    return total