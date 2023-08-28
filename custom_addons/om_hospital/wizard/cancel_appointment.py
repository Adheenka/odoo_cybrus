import datetime
from odoo import api,fields, models,_
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import  date
class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Apponintment" ,domain=[('state','=','draft'), ('priority','in',('0','1',False))])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        allowed_date = self.appointment_id.booking_time - relativedelta.relativedelta(days=int(cancel_day))
        if allowed_date < date.today():
            raise ValidationError(_("Sorry cancellation is not allowded for this booking!"))
        self.appointment_id.state = 'cancel'
        # if self.appointment_id.booking_time == fields.Date.today():
        #     raise ValidationError(_('sorry booing cancelation not allowed same day'))
        # self.appointment_id.state = 'cancel'
        # return
