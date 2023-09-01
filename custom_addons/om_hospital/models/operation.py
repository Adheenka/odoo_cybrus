from odoo import fields,models,api


class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Hospital Operation'
    _log_access = False
    _order = 'sequence,id'
    _rec_name = 'operation_name'

    doctor_id = fields.Many2one('res.users' , string="Doctor")
    sequence = fields.Integer(default=1,string="Sequence_no")
    operation_name = fields.Char(string="Name")

    reference_record = fields.Reference(
        selection=[('hospital.pateint', 'Patient'), ('hospital.appointment', 'Appointment')])
    # reference_record = fields.Reference(
    #     selection=[('hospital.patient', 'Hospital'), ('hospital.appointment', 'Appointment')])


    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]