


{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Sales/Sales',
    'author': 'adheen',
    'sequence': -100,
    'summary': 'Hospital management system',
    'description': """ Hospital management system
""",
    'depends': ['mail','product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/pateint_view.xml',
        'views/female_pateint_view.xml',
        'views/appoinment_view.xml',
        'views/odoo_playground_view.xml',
        'views/patient_tag_view.xml',
    ],
    'demo': [],
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}
