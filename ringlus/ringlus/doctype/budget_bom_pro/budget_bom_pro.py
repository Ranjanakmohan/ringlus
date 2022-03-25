# Copyright (c) 2022, jan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BudgetBOMPro(Document):
	pass
	# def get_rate(raw_material):
	# 	item_price = frappe.get_doc('Item Price', filters={"item_code": item_code })
  	# 	item = frappe.db.exists('Item Price',item_price.name)
  	# 	if item:
	# 		  return item_price.price_list_rate
  	# 	else:
	# 		  return "0"def get_rate(item):
  	# 	item_price = frappe.get_last_doc('Item Price', filters={"item_code": item , "price_list":"Standard Selling"})
  	# 	item = frappe.db.exists('Item Price',item_price.name)
  	# 	if item:
	# 		  return item_price.price_list_rate
  	# 	else:
	# 		  return "0"
@frappe.whitelist()
def test(item):
	data = frappe.db.sql("""select p.price_list_rate,p.name FROM `tabItem Price` p WHERE p.item_code=%s""",(item),as_dict=1)
	frappe.msgprint(int(data[0].get("price_list_rate")))
	return data[0].get("price_list_rate")
