from odoo import fields, models


class HospitalPateint(models.Model):
    _name = "hospital.pateint"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "hospital pateint"

    name = fields.Char(string='Name',tracking=True)
    ref = fields.Char(string='Reference',tracking=True)
    age = fields.Integer(string="Age",tracking=True)
    gender = fields.Selection([('male','Male'), ('female','Female')],string='Gender',tracking=True)
    active = fields.Boolean(string="Active",default=True)