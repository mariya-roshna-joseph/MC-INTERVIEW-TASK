# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Customer Payment Report',
    'version': '14.0',
    'summary': 'cCustomer Payment Details Report',
    'sequence': 10,
    'category': '',
    'description': 'Customer Payment Details Report',
    'depends': ['base', 'account'],
    'images': ['static/description/image.png'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/customer_payment_report_wizard.xml',
        'report/report.xml',
        'report/customer_payment_report.xml',
    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
