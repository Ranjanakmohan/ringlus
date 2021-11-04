import frappe

def validate_job_card(doc, method):
    for i in doc.time_logs:
        i.to_time = i.from_time