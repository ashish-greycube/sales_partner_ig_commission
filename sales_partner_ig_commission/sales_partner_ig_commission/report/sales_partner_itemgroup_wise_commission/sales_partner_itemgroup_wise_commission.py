# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
    return get_columns(), get_data(filters)

def get_columns():
    return [
        "PaymentDate:Date:100",
        "Customer:Link/Customer:130",
        "Amount:Currency:100",
        "PaymentEntryReference:Link/Payment Entry:120",
        "SalesInvoice:Link/Sales Invoice:100",
        "SalesPartner:Link/Sales Partner:120",
        "ItemGroup:Link/Item Group:120",
        "CommissionPercent:Percent:120",
        "CommissionAmount:Currency:120"
    ]

def get_data(filters):
    where_conditions = []
    if filters.get("from_date"):
        where_conditions.append("tpe.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        where_conditions.append("tpe.posting_date <= %(to_date)s")
    if filters.get("sales_partner"):
        where_conditions.append("c.default_sales_partner >= %(sales_partner)s")
    where_conditions = " and " + " and ".join(where_conditions)

    data = frappe.db.sql("""
select 
tpe.posting_date as "PaymentDate:Date:100",
tpe.party as "Customer:Link/Customer:130",
per.allocated_amount as "Amount:Currency:100",
tpe.name as "PaymentEntryReference:Link/Payment Entry:120",
per.reference_name as "SalesInvoice:Link/Sales Invoice:100",
c.default_sales_partner As "SalesPartner:Link/Sales Partner:120",
spigc.item_group as "ItemGroup:Link/Item Group:120", 
spigc.commission_percent as "CommissionPercent:Percent:120", 
(per.allocated_amount*spigc.commission_percent)/100 as "CommissionAmount:Currency:120"
from `tabPayment Entry` tpe 
inner join `tabPayment Entry Reference` per on per.parent = tpe.name
and per.reference_doctype = 'Sales Invoice'
inner join tabCustomer  AS c ON c.name = tpe.party
inner join `tabSales Invoice`  as si on per.reference_name = si.name
INNER JOIN (
    select parent, item_group
    from `tabSales Invoice Item`
    group by parent,item_group
    having count(distinct parent,item_group) = 1
) sit on sit.parent = si.name
INNER JOIN `tabSales Partner` AS sp on c.default_sales_partner = sp.name
INNER JOIN `tabItem Groupwise Commission CT` as spigc on spigc.parent = sp.name and sit.item_group = spigc.item_group
where tpe.payment_type='Receive' 
{where_conditions}
UNION ALL
select 
tpe.posting_date as PaymentDate,
tpe.party as Customer,
tpe.paid_amount as Amount,
tpe.name as PaymentEntryReference,
'' as SalesInvoice,
c.default_sales_partner As SalesPartner,
'' as ItemGroup, 
0 as CommissionPercent, 
0 as CommissionAmount
from `tabPayment Entry` tpe 
inner join tabCustomer  AS c ON c.name = tpe.party
INNER JOIN `tabSales Partner` AS sp on c.default_sales_partner = sp.name
where tpe.payment_type='Receive' and
tpe.name not in ( select distinct per.parent from `tabPayment Entry Reference` per )
{where_conditions}""".format(where_conditions=where_conditions), filters, as_dict=0)
    return data

