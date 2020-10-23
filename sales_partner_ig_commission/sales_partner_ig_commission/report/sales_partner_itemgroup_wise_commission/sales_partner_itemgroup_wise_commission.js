frappe.query_reports["Sales Partner ItemGroup Wise Commission"] = {
	"filters": [
		
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_end()
        },
        {
			"fieldname":"sales_partner",
			"label": __("Sales Partner"),
            "fieldtype": "Link",
            "options":"Sales Partner",
			"width": "200"
		}
	]
}