# -*- coding: utf-8 -*-

{
    'name': 'pos_inheritence',
    'version': '1.0.0',
    'category': 'Sales/Sales',
    'author': 'adheen',
    'sequence': -90,
    'summary': 'pos_inheritence',
    'description': """ pos management system
""",
    'depends': ['base','point_of_sale'],
    'data': [

        'views/res_partner_view.xml',
        'views/pos_bank_details.xml',
        'views/coupon.xml',





    ],
    'assets':{
        'web.assets_qweb': ['pos_inheritence/static/src/xml/*',
                            ],
        'web.assets_backend': ['pos_inheritence/static/src/js/*',
                               ],
    },

    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',


}

