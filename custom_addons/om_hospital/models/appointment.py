from odoo import fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "hospital appointment"
    pateint_id = fields.Many2one('hospital.pateint')