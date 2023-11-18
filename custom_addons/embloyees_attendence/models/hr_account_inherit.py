from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    @api.model
    # def automatic_check_out(self):
    #
    #     records = self.search([('check_out', '=', False),('check_in', '!=', False)], order='check_in desc', limit=1)
    #
    #     if records:
    #         latest_attendance = records[0]
    #
    #         working_hours_per_day = latest_attendance.employee_id.resource_calendar_id.hours_per_day
    #         automatic_checkout_threshold = timedelta(hours=working_hours_per_day)
    #         time_elapsed = datetime.now() - latest_attendance.check_in
    #         latest_attendance.worked_hours = time_elapsed.total_seconds() / 3600
    #
    #         if time_elapsed >= automatic_checkout_threshold:
    #             latest_attendance.check_out = datetime.now()
    #
    #     return True

    def automatic_check_out(self):
        # Find the latest attendance record for the current employee
        records = self.search([('check_out', '=', False), ('check_in', '!=', False)], order='check_in desc', limit=1)

        if records:
            latest_attendance = records[0]

            # Retrieve the working hours per day from the employee's calendar
            working_hours_per_day = latest_attendance.employee_id.resource_calendar_id.hours_per_day

            # Calculate the threshold for automatic checkout
            automatic_checkout_threshold = timedelta(hours=working_hours_per_day)

            # Calculate the time elapsed since the last check-in
            time_elapsed = datetime.now() - latest_attendance.check_in

            # Calculate the total worked hours in the same day
            total_worked_hours = latest_attendance.worked_hours + time_elapsed.total_seconds() / 3600

            # If the total worked hours exceed the automatic checkout threshold, check out
            if total_worked_hours >= working_hours_per_day:
                # Auto checkout
                latest_attendance.check_out = datetime.now()

        # Perform other necessary operations if needed
        # ...

        return True







    # @api.model
    # def automatic_check_out(self):
    #     # Find the latest attendance record for the current employee
    #     records = self.search([('check_out', '=', False), ('check_in', '!=', False)], order='check_in desc', limit=1)
    #
    #     if records:
    #         latest_attendance = records[0]
    #
    #         # Retrieve the working hours per day from the employee's calendar
    #         working_hours_per_day = latest_attendance.employee_id.resource_calendar_id.hours_per_day
    #
    #         # Calculate the threshold for automatic checkout
    #         automatic_checkout_threshold = timedelta(hours=working_hours_per_day)
    #
    #         # Calculate the time elapsed since check-in
    #         time_elapsed = datetime.now() - latest_attendance.check_in
    #
    #         # Save the worked hours in the worked_hours field
    #         latest_attendance.worked_hours = time_elapsed.total_seconds() / 3600
    #
    #         # If the time elapsed exceeds the automatic checkout threshold, check out
    #         if time_elapsed >= automatic_checkout_threshold:
    #             # Auto checkout
    #             latest_attendance.check_out = datetime.now()
    #
    #     # Perform other necessary operations if needed
    #     # ...
    #
    #     return True

