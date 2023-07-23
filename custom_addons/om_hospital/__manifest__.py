


{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Sales/Sales',
    'author': 'adheen',
    'sequence': -100,
    'summary': 'Hospital management system',
    'description': """ Hospital management system
""",
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/pateint_view.xml',
        'views/female_pateint_view.xml',
        'views/appoinment_view.xml'
    ],
    'demo': [],
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}
