import datetime
from odoo import models, fields, api

class ClassroomReportWizard(models.TransientModel):
    _name = 'classroom.report.wizard'
    _description = 'Classroom Report Wizard'

    from_date = fields.Date(string='Date From')
    to_date = fields.Date(string='Date To')
    dealer = fields.Many2one('res.partner', string='Dealer')

    def action_print_report(self):
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'dealer_id': self.dealer.id,
        }
        return self.env.ref('class_room.action_report_classroom').report_action(self, data=data)





