from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import datetime

class HospitalPateint(models.Model):
    _name = "hospital.pateint"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "hospital pateint"

    name = fields.Char(string='Name',tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='Reference',tracking=True)
    age = fields.Integer(string="Age",compute='_compute_age',inverse='_inverse_compute_age',tracking=True, search="_search_age")
    gender = fields.Selection([('male','Male'), ('female','Female')],string='Gender',tracking=True)
    active = fields.Boolean(string="Active",default=True)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag',string="Tag")
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count")
    appointment_ids = fields.One2many('hospital.appointment', 'pateint_id', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')])
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Birthday", compute='_compute_is_birthday')
    phone=fields.Char(string="Phone Number")
    email=fields.Char(string="Email")
    website=fields.Char(string="Website")

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        appointment_group = self.env['hospital.appointment'].read_group(domain=[], fields=['pateint_id'],
                                                                        groupby=['pateint_id'])
        for appointment in appointment_group:
            pateint_id = appointment.get('pateint_id')[0]
            patient_rec = self.browse(pateint_id)
            patient_rec.appointment_count = appointment['pateint_id_count']
            self -= patient_rec
        self.appointment_count = 0
    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #         for rec in self:
    #             rec.appointment_count = self.env['hospital.appointment'].search_count([('pateint_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Entered DOB is not accepttable"))
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.pateint')
        return super(HospitalPateint,self).create(vals)
    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.pateint.sequence')
        return super(HospitalPateint, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_date = date_of_birth.replace(day=1, month=1)
        end_date = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_date), ('date_of_birth', '<=', end_date)]
    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("you cannot delete a patient with appointments !"))

    def name_get(self):
        return [(record.id,'[%s] %s' %(record.ref,record.name)) for record in self]
    def action_test(self):
        print("clicked")
        return

    def action_view_appointment(self):
        return {
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form,calendar,activity',
            'context': {'default_pateint_id': self.id},
            'domain': [('pateint_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }