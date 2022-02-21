from . import __version__ as app_version

app_name = "ringlus"
app_title = "Ringlus"
app_publisher = "jan"
app_description = "Ringlus"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "janlloydangeles@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ringlus/css/ringlus.css"
# app_include_js = "/assets/ringlus/js/ringlus.js"

# include js, css files in header of web template
# web_include_css = "/assets/ringlus/css/ringlus.css"
# web_include_js = "/assets/ringlus/js/ringlus.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ringlus/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Purchase Order" : "public/js/purchase_order.js",
	"Quotation" : "public/js/quotation.js",
	"Material Request" : "public/js/material_request.js",
	"Sales Order" : "public/js/sales_order.js",
	"Additional Salary": "public/js/additional_salary.js",
	"Attendance Request": "public/js/attendance_request.js",

}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ringlus.install.before_install"
# after_install = "ringlus.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ringlus.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Quotation": {
		"on_submit": "ringlus.doc_events.quotation.submit_q",
		"on_cancel": "ringlus.doc_events.quotation.cancel_q",
	},
	"Material Request": {
		"validate": "ringlus.doc_events.material_request.validate_mr",
		"on_submit": "ringlus.doc_events.material_request.on_submit_mr",
		"on_cancel": "ringlus.doc_events.material_request.cancel_mr",
	},
	"Purchase Order": {
		"on_submit": "ringlus.doc_events.purchase_order.on_submit_po",
	},
	"Purchase Invoice": {
		"on_submit": "ringlus.doc_events.purchase_invoice.on_submit_pi",
	},
	"Purchase Receipt": {
		"on_submit": "ringlus.doc_events.purchase_receipt.on_submit_pr",
		"on_cancel": "ringlus.doc_events.purchase_receipt.on_cancel_pr",
	},
	"Sales Order": {
		"on_submit": "ringlus.doc_events.sales_order.on_submit_so",
		"on_cancel": "ringlus.doc_events.sales_order.on_cancel_so",
	},
	"Delivery Note": {
		"on_submit": "ringlus.doc_events.sales_order.on_submit_dn",
	},
	"Sales Invoice": {
		"on_submit": "ringlus.doc_events.purchase_invoice.on_submit_si",
	},
	"Job Card": {
		"on_submit": "ringlus.doc_events.job_card.validate_job_card",
	},
	"Stock Entry": {
		"on_submit": "ringlus.doc_events.stock_entry.on_submit_se",
	},
	"Opportunity": {
		"on_trash": "ringlus.doc_events.opportunity.on_trash_o",
	},
	"Addtional Salary": {
		"validate": "ringlus.doc_events.additional_salary.validate_as",
	}
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ringlus.tasks.all"
# 	],
# 	"daily": [
# 		"ringlus.tasks.daily"
# 	],
# 	"hourly": [
# 		"ringlus.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ringlus.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ringlus.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ringlus.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ringlus.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ringlus.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ringlus.auth.validate"
# ]

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Quotation-budget_bom",
                    "Quotation-reference",
                    "Quotation-budget_bom_reference",
                    "Quotation-opportunities",
                    "Quotation-budget_bom_opportunity",
                    "Quotation-additional_operating_cost",

					"Opportunity-budget_bom_reference",
                    "Opportunity-reference",

                    "Sales Order-budget_bom_reference",
                    "Sales Order-reference",
                    "Sales Order-additional_operating_cost",
                    "BOM-budget_bom",
                    "Material Request Item-budget_bom_rate",
                    "Material Request-budget_bom",
                    "Purchase Order Item-budget_bom_rate",

                    "Purchase Order-approve_po_rate",
                    "Workstation-operation_time",
                    "Opportunity-budget_bom",
                    "Purchase Order-budget_bom",
                    "Purchase Invoice-budget_bom",
                    "Purchase Receipt-budget_bom",
                    "Sales Invoice-budget_bom_reference",
                    "Sales Invoice-references",
                    "Delivery Note-budget_bom_reference",
                    "Delivery Note-references",
                    "BOM Item-operation_time_in_minutes",
                    "Material Request Item-budget_bom_raw_material",
                    "Purchase Invoice-budget_bom_reference",
                    "Purchase Invoice-reference",
                    "Purchase Receipt-reference",
                    "Purchase Receipt-budget_bom_reference",
					"Purchase Order-reference",
                    "Purchase Order-budget_bom_reference",
					"Material Request-reference_bom",
                    "Material Request-budget_bom_reference",

					"Quotation Item-column_break_16",
					"Quotation Item-column_break_26",
					"Quotation Item-estimated_bom_material_cost",
					"Quotation Item-estimated_bom_operation_cost",
					"Quotation Item-material_cost",
					"Quotation Item-material_margin",
					"Quotation Item-material_margin_amount",
					"Quotation Item-material_overhead",
					"Quotation Item-material_overhead_amount",
					"Quotation Item-operation_cost",
					"Quotation Item-operation_margin",
					"Quotation Item-operation_margin_amount",
					"Quotation Item-operation_overhead",
					"Quotation Item-operation_overhead_amount",
					"Quotation Item-section_break_11",
					"Quotation Item-section_break_21",
					"Quotation Item-total_cost",
					"Quotation Item-total_margin_cost",
					"Quotation Item-total_operation_cost",
					"Quotation-apply_default",

					"Quotation-additional_operating_cost",
					"Quotation-budget_bom_opportunity",
					"Quotation-budget_bom_reference",
					"Quotation-column_break_39",
					"Quotation-default_material_margin",
					"Quotation-default_material_overhead",
					"Quotation-default_operation_margin",
					"Quotation-default_operation_overhead",
					"Quotation-margin_and_overaged_values",
					"Quotation-opportunities",
					"Quotation-reference",

					"Work Order-budget_bom",

                    "Manufacturing Settings-default_operation",
					"Manufacturing Settings-default_workstation",
					"Manufacturing Settings-electrical_operation_time_in_minute",
					"Manufacturing Settings-cb_100",
					"Manufacturing Settings-mechanical_bom_default_operation",
                    "Manufacturing Settings-mechanical_bom_default_workstation",
					"Manufacturing Settings-mechanical_operation_time_in_minute",
					"Manufacturing Settings-cb_200",

					"Manufacturing Settings-fg_bom_default_operation",
					"Manufacturing Settings-fg_bom_default_workstation",
					"Manufacturing Settings-fg_operation_time_in_minute",

					"Manufacturing Settings-default_raw_material_warehouse",
					"Manufacturing Settings-budget_bom_defaults",

					"Sales Order Item-references",
					"Sales Order Item-project_code",
					"Sales Order-cost_center",
					"Sales Order-generate_project_code",
					"Item-item_category",

					"Attendance Request-salary_structure",
                    "Attendance Request-base",
                    "Attendance Request-overtime_hour",
                    "Attendance Request-overtime_amount",


                    "Additional Salary-additional_request_reference",
                    "Additional Salary-additional_request",
                    "Additional Salary-fetch_attendance_requests",
                    "Additional Salary-is_hour_based",
                    "Additional Salary-total_working_hour",
                    "Employee-overtime_multiplication_factor",
                    "Attendance Request-overtime_multiplication_factor",
                    "Attendance Request-additional_salary",
                    "Global Defaults-default_project_code",

                    "Quotation-total_product_cost_of_sale",
                    "Quotation-total_sale_value",
                    "Quotation-column_break_48",
                    "Quotation-total_gross_profit_amount",
                    "Quotation-gross_profit_percentage",
				]
			]
		]
	},
	{
		"doctype": "Property Setter",
		"filters": [
			[
				"name",
				"in",
				[
					"Purchase Order Item-schedule_date-in_list_view",
					"Work Order-additional_operating_cost-fetch_from",
					"Work Order-additional_operating_cost-fetch_if_empty",
					"Material Request Item-conversion_factor-precision",
					"Material Request Item-qty-precision",
					"Purchase Order Item-qty-precision",
					"Purchase Receipt Item-qty-precision",
					"Purchase Invoice Item-qty-precision",
					"Attendance Request-to_date-read_only",
				]
			]
		]
	}
]