import datetime
from odoo import models, fields, api

class ClassroomReportWizard(models.TransientModel):
    _name = 'classroom.report.wizard'
    _description = 'Classroom Report Wizard'

    from_date = fields.Date(string='Date From')
    to_date = fields.Date(string='Date To')
    dealer = fields.Many2one('res.partner', string='Dealer')

    def action_print_report(self):
        report_data = {
            'doc_ids': [self.id],
            'doc_model': 'classroom',
            'docs': self,
        }
        return self.env.ref('class_room.action_report_student').report_action(self, data=report_data)
    # def action_print_report(self):
    #     student_details = self.env['classroom'].search_read([])
    #     data = {
    #         'form':self.read()[0],
    #         'student_details': 'student_details',
    #         'docs': self,
    #     }
    #     return self.env.ref('class_room.action_report_student').report_action(self, data=data)





