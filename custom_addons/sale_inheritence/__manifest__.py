# -*- coding: utf-8 -*-

{
    'name': 'sale_inheritence',
    'version': '1.0.0',
    'category': 'Sales/Sales',
    'author': 'adheen',
    'sequence': -90,
    'summary': 'sa8e_inheritence',
    'description': """ sale management system
""",
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence_data.xml',
        'data/mail_template_date.xml',
        'data/invoice_sms_template.xml',
        'views/estimation_view.xml',
        'views/description_view.xml',
        'views/sale_order_inherit.xml',
        'views/account_move_inherit.xml',
        'views/sale_view.xml',

        'views/colour_view.xml',
        'views/job_order_views.xml',
        'report/report.xml',
        'report/job_order_card.xml',









    ],


    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',


}

