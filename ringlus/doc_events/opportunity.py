import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_bb(source_name, target_doc=None):
    doc = get_mapped_doc("Opportunity", source_name, {
        "Opportunity": {
            "doctype": "Budget BOM",
            "field_map":{
                "party_name": "customer"
            }
        }
    }, ignore_permissions=True)

    return doc

@frappe.whitelist()
def on_trash_o(doc, method):
    for i in doc.budget_bom_reference:
        frappe.db.sql(""" UPDATE `tabBudget BOM` SET opportunity='' WHERE name=%s""", i.budget_bom)
        frappe.db.commit()