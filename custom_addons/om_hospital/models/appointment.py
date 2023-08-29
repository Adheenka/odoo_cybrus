from odoo import api,fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'name'
    _order = 'id desc'



    # name = fields.Char(string="Sequence", required=True, copy=False,
    #                    readonly=True,
    #                    index=True, default=lambda self: _('New'))
    name = fields.Char(string="Sequence", required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    pateint_id = fields.Many2one('hospital.pateint',ondelete='cascade')
    ref = fields.Char(string='Reference', tracking=True)
    gender = fields.Selection(related='pateint_id.gender',readonly=False)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_time = fields.Date(string='Booking Date', default=fields.Date.context_today)
    prescription = fields.Html(string="Prescription")
    doctor_id = fields.Many2one('res.users', string='Docter',tracking=True)
    operation = fields.Many2one('hospital.operation', string="Operation")
    # sequence = fields.Char(string="Sequence", readonly=True, copy=False)

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],default='draft',required=True, string="status",tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price =fields.Boolean(striing="HIde Sales Price")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'hospital.appointment') or _('New')
            result = super(HospitalAppointment, self).create(vals)
            return result
    # @api.model
    # def create(self, vals):
    #    if vals.get('name', 'New') == 'New':
    #        vals['name'] = self.env['ir.sequence'].next_by_code(
    #            'hospital.pateint.sequence') or 'New'
    #    result = super(HospitalAppointment, self).create(vals)
    #    return result
    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    #     return super(HospitalAppointment, self).create(vals)



    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'New') == 'New':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
    #     return super(HospitalAppointment, self).create(vals)
    @api.onchange('pateint_id')
    def onchange_pateint_id(self):
        self.ref = self.pateint_id.ref

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You can delete appointment only in 'Draft' state"))
            return super(HospitalAppointment, self).unlink()
    def action_test(self):
        print("button")
        return {
            'effect':{
                'fadout':'slow',
                'messege':'click sucessful',
                'type':'rainbow_man'
            }
        }
    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'
    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"

    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.lst_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment')