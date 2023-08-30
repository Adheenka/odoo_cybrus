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
    # @http.route('/create/webstudent', type="http", auth="public", website=True)
    # def create_webstudent(self, **post):
    #     name = post.get('name')
    #     email = post.get('email')
    #     phone = post.get('phone')
    #     dob = post.get('dob')
    #
    #     # Create a student record
    #     classroom_model = request.env['classroom']
    #     new_student = classroom_model.sudo().create({
    #         'name': name,
    #         'email': email,
    #         'phone': phone,
    #         'dob': dob,
    #
    #         # Add other fields as needed
    #     })
    #
    #     return http.request.render('class_room.student_thanks', {})
    @http.route('/create/webstudent', type="http", auth="public", website=True)
    def create_webstudent(self, **post):
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        dob = post.get('dob')


        # Create a student record
        classroom_model = http.request.env['classroom']
        new_student = classroom_model.sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'dob': dob,
        })

        return http.request.render('class_room.student_thanks', {})