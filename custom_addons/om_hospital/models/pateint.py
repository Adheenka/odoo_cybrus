from datetime import date
from odoo import api, fields, models


class HospitalPateint(models.Model):
    _name = "hospital.pateint"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "hospital pateint"

    name = fields.Char(string='Name',tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='Reference',tracking=True)
    age = fields.Integer(string="Age",compute='_compute_age',tracking=True)
    gender = fields.Selection([('male','Male'), ('female','Female')],string='Gender',tracking=True)
    active = fields.Boolean(string="Active",default=True)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag',string="Tag")


    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.pateint')
        return super(HospitalPateint,self).create(vals)
    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0