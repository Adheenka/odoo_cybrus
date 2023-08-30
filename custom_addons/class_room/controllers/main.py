from odoo import http
from odoo.http import request

class Classroom(http.Controller):

    # Sample Controller Created
    @http.route('/student_webform', type="http",auth="public",website=True)
    def student_webfrom(self, **kw):
        # return "Thanks for watching"
        # patients = request.env['classroom'].sudo().search([])
        return http.request.render('class_room.create_student', {})

    @http.route('/create/webstudent', type="http",auth="public",website=True)
    def update_patient(self, **kw):
        request.env['classroom'].sudo().create(kw)
        return request.render("class_room.student_thanks", {})
