import datetime
from odoo import api,fields, models



class GenerateReportWizard(models.TransientModel):
    _name = "classroom.report"
    _description = "Generate Report Wizard"

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    classroom_id = fields.Many2one('classroom',string="classroom")

    def action_print_report(self):
        classroom = self.env['classroom'].search_read([])
        data = {
            'form': self.read()[0],
            'classroom': classroom,
        }
        return self.env.ref('class_room.action_print_report').report_action(self, data=data)
