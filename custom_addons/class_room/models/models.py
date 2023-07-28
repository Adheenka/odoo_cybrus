# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api


class Classroom(models.Model):
    _name = "classroom"
    _description = "Classroom Model"

    name = fields.Char(string="Name")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(compute="_compute_age", store=True)

    marklist = fields.One2many("marklist", "classroom_id", string="Marklist")
    # Add new field
    address = fields.Char(string="Address")
    address_street = fields.Char(string='Street')
    address_street2 = fields.Char(string='Street 2')
    address_city = fields.Char(string='City')
    address_pincode = fields.Char(string='Pincode')
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=', country_id)]")
    total_marks_all = fields.Float(string='Total Marks (All)', compute='_compute_total_marks_all', store=True)

    @api.depends('marklist.total')
    def _compute_total_marks_all(self):
        for classroom in self:
            classroom.total_marks_all = sum(classroom.marklist.mapped('total'))
    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0
    # @api.onchange("dob")
    # def _compute_age(self):
    #     for classroom in self:
    #         if classroom.dob:
    #             classroom.age = (fields.Date.today() - classroom.dob).days // 365




class Marklist(models.Model):
    _name = "marklist"
    _description = "Marklist Model"

    classroom_id = fields.Many2one("classroom", string="Classroom")
    exam_name = fields.Char(string="Exam Name")
    subject1 = fields.Float(string="Subject 1")
    subject2 = fields.Float(string="Subject 2")
    subject3 = fields.Float(string="Subject 3")
    subject4 = fields.Float(string="Subject 4")
    total = fields.Float(compute="_compute_total", store=True)
    average = fields.Float(compute="_compute_average", store=True)
    total_marks = fields.Float(compute="_compute_total_marks", store=True)

    @api.depends("subject1", "subject2", "subject3", "subject4")
    def _compute_total(self):
        for marklist in self:
            marklist.total = marklist.subject1 + marklist.subject2 + marklist.subject3 + marklist.subject4

    @api.depends("total")
    def _compute_average(self):
        for marklist in self:
            marklist.average = marklist.total / 4

    @api.depends("subject1", "subject2", "subject3", "subject4")
    def _compute_total_marks(self):
        for marklist in self:
            marklist.total = marklist.subject1 + marklist.subject2 + marklist.subject3 + marklist.subject4
class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_states_for_country(self, country_id):
        country = self.env['res.country'].browse(country_id)
        states = self.env['res.country.state'].search([('country_id', '=', country.id)])
        return states