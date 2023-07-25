from odoo import api,fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    pateint_id = fields.Many2one('hospital.pateint')
    ref = fields.Char(string='Reference', tracking=True)
    gender = fields.Selection(related='pateint_id.gender',readonly=False)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_time = fields.Date(string='Booking Date', default=fields.Date.context_today)

    @api.onchange('pateint_id')
    def onchange_pateint_id(self):
        self.ref = self.pateint_id.ref
