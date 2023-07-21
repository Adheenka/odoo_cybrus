from odoo import fields, models


class HospitalPateint(models.Model):
    _name = "hospital.pateint"
    _description = "hospital pateint"

    name = fields.Char(string='Name')
    ref = fields.Char(string='Reference')
    age = fields.Integer(string="Age")
    gender = fields.Selection([('male','Male'), ('female','Female')],string='Gender')
    active = fields.Boolean(string="Active",default=True)