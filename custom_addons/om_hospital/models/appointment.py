from odoo import api,fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'pateint_id'

    pateint_id = fields.Many2one('hospital.pateint')
    ref = fields.Char(string='Reference', tracking=True)
    gender = fields.Selection(related='pateint_id.gender',readonly=False)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_time = fields.Date(string='Booking Date', default=fields.Date.context_today)
    prescription = fields.Html(string="Prescription")
    doctor_id = fields.Many2one('res.users', string='Docter')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],default='draft',required=True, string="status")

    @api.onchange('pateint_id')
    def onchange_pateint_id(self):
        self.ref = self.pateint_id.ref

    def action_test(self):
        print("button")
        return {
            'effect':{
                'fadout':'slow',
                'messege':'click sucessful',
                'type':'rainbow_man'
            }
        }