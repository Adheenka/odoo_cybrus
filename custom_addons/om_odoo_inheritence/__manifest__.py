# -*- coding: utf-8 -*-

{
    'name': 'om_odoo_inheritence',
    'version': '1.0.0',

    'author': 'adheen',
    'sequence': -50,
    'summary': 'odoo_sale_inherit',
    'description': """ sale management system
""",
    'depends': ['sale','crm'],
    'data': [

        'views/sale_order_view.xml',
        'views/account_move_view.xml',

    ],
    'demo': [],
    'auto_install': False,
    'application': True,


}

