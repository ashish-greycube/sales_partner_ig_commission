from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	config = [
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"name": "Sales Partner ItemGroup Wise Commission",
					"is_query_report": True,
					"doctype": "Sales Invoice"
				}
			]
		}
		]
	return config
	