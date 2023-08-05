from odoo import models


class StudentCardXLS(models.AbstractModel):
    _name = 'report.class_room.report_student_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 9, 'align': 'vcenter','bold': True})
        format2 = workbook.add_format({'font_size': 9, 'align': 'vcenter'})
        date_format = workbook.add_format({'font_size': 9,'num_format': 'mm/dd/yyyy', 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Student Execl Report')

        # Header
        header_format = workbook.add_format({'font_size': 14, 'align': 'center', 'bold': True})
        sheet.merge_range('C2:E2', 'Student Excel Report', header_format)

        sheet.write(3, 2, 'Name', format1)
        sheet.write(3, 3, lines.name, format2)
        sheet.write(4, 2, 'Age', format1)
        sheet.write(4, 3, lines.age, format2)
        sheet.write(5, 2, 'DOB', format1)
        sheet.write(5, 3, lines.dob.strftime('%m/%d/%Y'), date_format)

        sheet.write(3, 6, 'Address', format1)
        sheet.write(3, 7, lines.address_street, format2)
        sheet.write(4, 7, lines.address_street2, format2)
        sheet.write(5, 7, lines.address_pincode, format2)
        sheet.write(5, 8, lines.country_id.name, format2)
        sheet.write(6, 7, lines.state_id.name, format2)

        sheet.write(8, 2, 'Marklist', format1)
        sheet.write(9, 2, 'Exam', format1)
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
            row += 1

        total_marks_format = workbook.add_format({'font_size': 12, 'align': 'vcenter'})
        sheet.merge_range(row + 1, 2, row + 1, 7, 'Total Marks (All)', total_marks_format)
        sheet.write(row + 1, 8, lines.total_marks_all, format2)