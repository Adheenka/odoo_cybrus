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
        'data/sequence_data.xml',
        'views/estimation_view.xml',
        'views/description_view.xml',
        'views/sale_view.xml',








    ],
    # 'assets':{
    #     'web.assets_qweb': ['pos_inheritence/static/src/xml/*',
    #                         ],
    #     'web.assets_backend': ['pos_inheritence/static/src/js/*',
    #                            ],
    # },

    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',


}

