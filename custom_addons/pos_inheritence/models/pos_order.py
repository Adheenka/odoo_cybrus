from odoo import fields, models

class PosOrderExtend(models.Model):
    _inherit = 'pos.order'

    dob = fields.Date(string='Date of Birth', related='partner_id.dob', store=True, readonly=True)
    mobile = fields.Char(string='Mobile number', related='partner_id.mobile', store=True, readonly=True)
