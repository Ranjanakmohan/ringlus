import frappe

def on_submit_so(doc, method):
    for i in doc.budget_bom_reference:
        if i.budget_bom:
            frappe.db.sql(""" UPDATE `tabBudget BOM` SET status=%s WHERE name=%s  """, ("To Material Request", i.budget_bom))
            frappe.db.commit()


def on_submit_dn(doc, method):
    doctype = "Delivery Note" if doc.doctype == 'Sales Invoice' else doc.doctype
    for i in doc.budget_bom_reference:
        if i.budget_bom:
            frappe.db.sql(""" UPDATE `tabBudget BOM` SET status=%s WHERE name=%s  """,
                          ("To Bill ", i.budget_bom))
            frappe.db.commit()

def update_budget_bom(i):
    if i.budget_bom:
        budget_bom = frappe.db.sql(""" SELECT * FROM `tabBudget BOM` WHERE name=%s""", i.budget_bom, as_dict=1)
        status = ""
        if budget_bom[0].status == "To PO and SO":
            status = "To SO"

        elif budget_bom[0].status == "To PO":
            status = "Completed"

        frappe.db.sql(""" UPDATE `tabBudget BOM` SET status=%s WHERE name=%s""",(status, i.budget_bom))
        frappe.db.commit()

def on_cancel_so(doc, method):
    for i in doc.budget_bom_reference:
        if i.budget_bom:
            frappe.db.sql(""" UPDATE `tabBudget BOM` SET status=%s WHERE name=%s  """,("Quotation In Progress", i.budget_bom))
            frappe.db.commit()