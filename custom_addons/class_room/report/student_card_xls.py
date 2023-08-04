from odoo import models


class StudentCardXLS(models.AbstractModel):
    _name = 'report.class_room.report_student_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 11, 'align': 'vcenter'})
        format2 = workbook.add_format({'font_size': 9, 'align': 'vcenter'})
        date_format = workbook.add_format({'font_size': 9,'num_format': 'mm/dd/yyyy', 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Student Card')
        sheet.write(2, 2, 'Name', format1)
        sheet.write(2, 3, lines.name, format2)
        sheet.write(3, 2, 'Age', format1)
        sheet.write(3, 3, lines.age, format2)
        sheet.write(4, 2, 'Date of Birth', format1)
        sheet.write(4, 3, lines.dob.strftime('%m/%d/%Y'), date_format)

        sheet.write(2, 5, 'Address', format1)
        sheet.write(2, 6, lines.address_street, format2)
        sheet.write(3, 6, lines.address_street2, format2)
        sheet.write(4, 6, lines.address_pincode, format2)
        sheet.write(4, 7, lines.country_id.name, format2)
        sheet.write(4, 8, lines.state_id.name, format2)

        sheet.write(8, 2, 'Marklist', format1)
        sheet.write(9, 2, 'Exam Name', format1)
        sheet.write(9, 3, 'Subject 1', format1)
        sheet.write(9, 4, 'Subject 2', format1)
        sheet.write(9, 5, 'Subject 3', format1)
        sheet.write(9, 6, 'Subject 4', format1)
        sheet.write(9, 7, 'Total', format1)
        sheet.write(9, 8, 'Average', format1)

        row = 11
        for mark in lines.marklist:
            sheet.write(row, 2, mark.exam_name, format2)
            sheet.write(row, 3, mark.subject1, format2)
            sheet.write(row, 4, mark.subject2, format2)
            sheet.write(row, 5, mark.subject3, format2)
            sheet.write(row, 6, mark.subject4, format2)
            sheet.write(row, 7, mark.total, format2)
            sheet.write(row, 8, mark.average, format2)
            row += 2

        sheet.write(row, 7, 'Total Marks (All):', format1)
        sheet.write(row, 8, lines.total_marks_all, format2)