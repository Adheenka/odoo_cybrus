from odoo import fields, models

class CustomResPartner(models.Model):
    _inherit = 'res.partner'

    dob = fields.Date(string='Date of Birth')
    mobile = fields.Char(string='Mobile number')
