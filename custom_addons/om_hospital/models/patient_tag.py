from odoo import api, fields, models


class PateintTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active',default=True)
    color = fields.Integer(string="color")
    color_2 = fields.Char(string="color_2")