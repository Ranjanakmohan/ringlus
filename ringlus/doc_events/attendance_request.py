import frappe

@frappe.whitelist()
def get_ss(employee):
    ss = frappe.db.sql(""" SELECT * FROm `tabSalary Structure Assignment` WHERE employee=%s and docstatus=1 ORDER BY name DESC LIMIT 1""", employee, as_dict=1)
    print('sssssssssssssssssssssssss')
    print(ss)
    return ss[0].salary_structure if len(ss) > 0 else "", ss[0].base if len(ss) > 0 else ""