from odoo import fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Hospital Appointment"
    pateint_id = fields.Many2one('hospital.pateint')
    appointment_time = fields.Datetime(string='Appointment Time')
    booking_time = fields.Date(string='Booking Date')