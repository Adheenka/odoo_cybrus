# -*- coding: utf-8 -*-

{
    'name': 'Multilevel_approval_system',
    'version': '1.0.0',
    'category': 'Inventory/Management',
    'author': 'adheen',
    'sequence': -96,
    'summary': 'Manage material requisitions and expenses',
    'description': """
       This module enhances Odoo by adding features for managing material requisitions and expenses in an organized manner.
       It includes functionalities such as creating and tracking material requisitions, managing expenses, and more.
   """,
    'depends': ['base','stock','sale_stock', 'hr','mail','sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence_data.xml',



        'views/purchase_approval.xml',

    ],


    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',


}

