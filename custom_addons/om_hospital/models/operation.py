from odoo import fields,models,api


class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Hospital Operation'
    _log_access=False
    # _order = 'sequence,id'

    doctor_id = fields.Many2one('res.users' , string="Doctor")

    operation_name = fields.Char(string="Name")
    # reference_record = fields.Reference(
    #     selection=[('hospital.patient', 'Hospital'), ('hospital.appointment', 'Appointment')])
    # sequence = fields.Integer(string="Sequence", default=1)

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]