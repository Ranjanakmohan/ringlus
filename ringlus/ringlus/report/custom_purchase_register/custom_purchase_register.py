# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _, msgprint
from frappe.utils import flt

from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
	get_dimension_with_children,
)


def execute(filters=None):
	return _execute(filters)

def _execute(filters=None, additional_table_columns=None, additional_query_columns=None):
	if not filters: filters = {}

	invoice_list = get_invoices(filters)
	columns = get_columns()
	if not invoice_list:
		msgprint(_("No record found"))
		return columns, invoice_list

	data = []
	added_tax = []
	sno = 1
	for inv in invoice_list:
		inv.serial_no = sno
		tax_accounts = frappe.db.sql(""" SELECT * FROM `tabPurchase Taxes and Charges` WHERE parent=%s """, inv.name, as_dict=1)

		for tax_acc in tax_accounts:

			if tax_acc not in added_tax:
				columns.append({"label": _(tax_acc.account_head),"fieldname": tax_acc.account_head,"fieldtype": "Data","width": 250})
				added_tax.append(tax_acc)

			inv[tax_acc.account_head] = tax_acc.tax_amount

		data.append(inv)
		sno +=1
	columns += [
		{"label": _("Round Off"), "fieldname": "round_off", "fieldtype": "Currency", "width": 150},
		{"label": _("Grand Total"), "fieldname": "grand_total", "fieldtype": "Currency", "width": 150},
		{"label": _("Rounded Total"), "fieldname": "rounded_total", "fieldtype": "Currency", "width": 150},

	]
	return columns, data


def get_columns():
	"""return columns based on filters"""
	columns = [
		{"label": _("Serial No"),"fieldname": "serial_no","fieldtype": "Data","width": 100},
		{"label": _("Posting Date"),"fieldname": "posting_date","fieldtype": "Date","width": 150},
		{"label": _("Supplier Invoice date"),"fieldname": "bill_date","fieldtype": "Date", "options": "Purchase Invoice","width": 200},
		{"label": _("Supplier Name"),"fieldname": "supplier_name","fieldtype": "Data", "options": "Purchase Invoice","width": 150},
		{"label": _("Invoice No"),"fieldname": "name","fieldtype": "Link", "options": "Purchase Invoice","width": 200},
		{"label": _("Net Total"),"fieldname": "net_total","fieldtype": "Currency","width": 150},
	]


	return columns

def get_conditions(filters):
	conditions = ""

	if filters.get("company"): conditions += " and company=%(company)s"
	if filters.get("supplier"): conditions += " and supplier = %(supplier)s"

	if filters.get("from_date"): conditions += " and posting_date>=%(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date<=%(to_date)s"

	if filters.get("mode_of_payment"): conditions += " and ifnull(mode_of_payment, '') = %(mode_of_payment)s"

	if filters.get("cost_center"):
		conditions +=  """ and exists(select name from `tabPurchase Invoice Item`
			 where parent=`tabPurchase Invoice`.name
			 	and ifnull(`tabPurchase Invoice Item`.cost_center, '') = %(cost_center)s)"""

	if filters.get("warehouse"):
		conditions +=  """ and exists(select name from `tabPurchase Invoice Item`
			 where parent=`tabPurchase Invoice`.name
			 	and ifnull(`tabPurchase Invoice Item`.warehouse, '') = %(warehouse)s)"""

	if filters.get("item_group"):
		conditions +=  """ and exists(select name from `tabPurchase Invoice Item`
			 where parent=`tabPurchase Invoice`.name
			 	and ifnull(`tabPurchase Invoice Item`.item_group, '') = %(item_group)s)"""

	accounting_dimensions = get_accounting_dimensions(as_list=False)

	if accounting_dimensions:
		common_condition = """
			and exists(select name from `tabPurchase Invoice Item`
				where parent=`tabPurchase Invoice`.name
			"""
		for dimension in accounting_dimensions:
			if filters.get(dimension.fieldname):
				if frappe.get_cached_value('DocType', dimension.document_type, 'is_tree'):
					filters[dimension.fieldname] = get_dimension_with_children(dimension.document_type,
						filters.get(dimension.fieldname))

					conditions += common_condition + "and ifnull(`tabPurchase Invoice Item`.{0}, '') in %({0})s)".format(dimension.fieldname)
				else:
					conditions += common_condition + "and ifnull(`tabPurchase Invoice Item`.{0}, '') in (%({0})s))".format(dimension.fieldname)

	return conditions

def get_invoices(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		select
			name, posting_date, credit_to, supplier, supplier_name, tax_id, bill_no, bill_date,
			remarks, base_net_total, grand_total, outstanding_amount,
			mode_of_payment, total as net_total, rounded_total, rounding_adjustment as round_off
		from `tabPurchase Invoice`
		where docstatus = 1 {0}
		order by posting_date desc, name desc""".format(conditions),filters, as_dict=1)
