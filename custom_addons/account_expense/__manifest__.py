# -*- coding: utf-8 -*-

{
    'name': 'account_expense_module',
    'version': '1.0.0',
    'category': 'Sales/Sales',
    'author': 'adheen',
    'sequence': -91,
    'summary': 'account_move_inheritence',
    'description': """ for account expense manegment system
""",
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',

        'views/account_expence.xml',










    ],


    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',


}

