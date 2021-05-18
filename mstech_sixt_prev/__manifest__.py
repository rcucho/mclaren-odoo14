# -*- coding: utf-8 -*-

{
    'name': 'Odoo - Sixt McLaren',
    'category': 'Technical Configuration',
    'author': 'Mouse Technologies',
    'summary':'Odoo - Sixt McLaren',
    'license': 'LGPL-3',
    'website': 'https://www.mstech.pe',
    'depends': [
        'account_fleet',
        'sale_crm',
    ],
    'data': [
        'data/sale_data.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'sequence': 1,
}

