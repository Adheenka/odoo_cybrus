
from odoo import models, fields, api, _


class ClassroomReportWizard(models.TransientModel):
    _name = 'classroom.report.wizard'
    _description = 'Classroom Report Wizard'


    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    # dealer = fields.Many2one('res.partner', string='Dealer')

    def action_print_report(self):
        domain = []

        start_date = self.start_date
        if start_date:
            domain += [('date', '>=', start_date)]

        end_date = self.end_date
        if end_date:
            domain += [('date', '<=', end_date)]

        student_detail = self.env['classroom'].search_read(domain)
        data = {
            'form': {
                'start_date': self.start_date,
                'end_date': self.end_date,
            },
            'student_detail': student_detail,
        }

        return self.env.ref('class_room.action_report_student').report_action(self, data=data)






