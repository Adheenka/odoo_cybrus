# -*- coding: utf-8 -*-
{
    'name': "School Management'",

    'summary': """ this module helping school management
        """,

    'description': """
        class room management system
    """,
    'sequence': -10,
    'author': "My Company",

    'category': 'Classroom',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menu.xml',
        'report/report.xml',
        'report/student_card.xml',



    ],
    # only loaded in demonstration mode
    'demo': [],

    'auto_install': False,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
