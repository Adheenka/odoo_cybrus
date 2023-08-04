from odoo import models


class StudentCardXLS(models.AbstractModel):
    _name = 'reports.class_room.student_card_xls'
    _inherit = 'reports.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print("Lines", lines, data)
        format1 = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 11, 'align': 'vcenter'})
        format3 = workbook.add_format({'font_size': 11, 'align': 'vright'})
        sheet = workbook.add_worksheet('Patient Card')
        sheet.write(0, 1, 'Name', format1)
        sheet.write(0, 2, lines.patient_name, format2)
        sheet.write(1, 1, 'Age', format1)
        sheet.write(1, 2, lines.patient_age, format3)
        sheet.write(2, 1, 'Email', format1)
        sheet.write(2, 2, lines.email_id, format2)