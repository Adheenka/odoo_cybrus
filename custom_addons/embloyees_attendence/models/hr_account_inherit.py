from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    def automatic_check_out(self):
        # Find the latest attendance record for the current employee
        latest_attendance = self.search([
            ('employee_id', '=', self.env.user.employee_id.id),
        ], order='check_in desc', limit=1)

        if latest_attendance:
            # Retrieve the working hours per day from the employee's calendar
            working_hours_per_day = latest_attendance.employee_id.resource_calendar_id.hours_per_day

            # Calculate the threshold for automatic checkout
            automatic_checkout_threshold = timedelta(hours=working_hours_per_day)

            # Calculate the time elapsed since check-in
            time_elapsed = datetime.now() - latest_attendance.check_in

            if time_elapsed >= automatic_checkout_threshold:
                # Auto checkout if the time elapsed exceeds the threshold
                latest_attendance.check_out = datetime.now()

        # Perform other necessary operations if needed
        # ...

        return True