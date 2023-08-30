from odoo import http
from odoo.http import request

class Classroom(http.Controller):

    # Sample Controller Created
    @http.route('/student_webform', type="http",auth="public",website=True)
    def student_webfrom(self, **kw):
        # return "Thanks for watching"
        # patients = request.env['classroom'].sudo().search([])
        return http.request.render('class_room.create_student', {})

    # @http.route('/create/webstudent', type="http", auth="public",website=True)
    # def update_patient(self, **kw):
    #     request.env['classroom'].sudo().create(kw)
    #     return request.render("class_room.student_thanks", {})
    @http.route('/create/webstudent', type="http", auth="public", website=True)
    def create_webstudent(self, **post):
        student_name = post.get('student_name')
        email = post.get('email')

        # Create a student record
        classroom_model = request.env['classroom']
        new_student = classroom_model.sudo().create({
            'name': student_name,
            'email': email,
            # Add other fields as needed
        })

        return http.request.render('class_room.student_thanks', {})
