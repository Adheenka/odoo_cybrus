from odoo import models


class StudentCardXLS(models.AbstractModel):
    _name = 'report.class_room.report_student_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Student Card')
        sheet.write(2, 2, 'Name', format1)
        sheet.write(2, 3, lines.name, format2)
        sheet.write(3, 2, 'Age', format1)
        sheet.write(3, 3, lines.age, format2)
        sheet.write(4, 2, 'Date of Birth', format1)
        sheet.write(4, 3, lines.dob, format2)

        sheet.write(6, 2, 'Address', format1)
        sheet.write(6, 3, lines.address, format2)
        sheet.write(7, 3, lines.address_street, format2)
        sheet.write(8, 3, lines.address_street2, format2)
        sheet.write(9, 3, lines.address_pincode, format2)
        sheet.write(9, 4, lines.country_id.name, format2)
        sheet.write(9, 5, lines.state_id.name, format2)

        sheet.write(11, 2, 'Marklist', format1)
        sheet.write(12, 2, 'Exam Name', format1)
        sheet.write(12, 3, 'Subject 1', format1)
        sheet.write(12, 4, 'Subject 2', format1)
        sheet.write(12, 5, 'Subject 3', format1)
        sheet.write(12, 6, 'Subject 4', format1)
        sheet.write(12, 7, 'Total', format1)
        sheet.write(12, 8, 'Average', format1)

        row = 13
        for mark in lines.marklist:
            sheet.write(row, 2, mark.exam_name, format2)
            sheet.write(row, 3, mark.subject1, format2)
            sheet.write(row, 4, mark.subject2, format2)
            sheet.write(row, 5, mark.subject3, format2)
            sheet.write(row, 6, mark.subject4, format2)
            sheet.write(row, 7, mark.total, format2)
            sheet.write(row, 8, mark.average, format2)
            row += 1

        sheet.write(row, 2, 'Total Marks (All):', format1)
        sheet.write(row, 3, lines.total_marks_all, format2)