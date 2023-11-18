# -*- coding: utf-8 -*-

{
    'name': 'Material Requisition Management',
    'version': '1.0.0',
    'category': 'Inventory/Management',
    'author': 'adheen',
    'sequence': -97,
    'summary': 'Manage material requisitions and expenses',
    'description': """
       This module enhances Odoo by adding features for managing material requisitions and expenses in an organized manner.
       It includes functionalities such as creating and tracking material requisitions, managing expenses, and more.
   """,
    'depends': ['base','stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/menu.xml',
        'views/material_requisition.xml',

    ],


    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',


}

