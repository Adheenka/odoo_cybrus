# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api


class Classroom(models.Model):
    _name = 'school_management.classroom'
    _description = 'Classroom Model'

    name = fields.Char(string='Name', required=True)
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    address = fields.Text(string='Address')
    marklist = fields.One2many('school_management.marklist', 'classroom_id', string='Marklist')

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:

                today = fields.Date.today()
                dob = fields.Datetime.from_string(record.dob)
                record.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @api.depends('marklist.subject_1', 'marklist.subject_2', 'marklist.subject_3', 'marklist.subject_4')
    def _compute_total(self):
        for record in self:
            if record.marklist:
                record.total = sum([record.marklist.subject_1, record.marklist.subject_2,
                                    record.marklist.subject_3, record.marklist.subject_4])

    @api.depends('total')
    def _compute_average(self):
        for record in self:
            record.average = record.total / 4.0

    total = fields.Float(string='Total Marks', compute='_compute_total', store=True)
    average = fields.Float(string='Average', compute='_compute_average', store=True)

class Marklist(models.Model):
    _name = 'school_management.marklist'
    _description = 'Marklist Model'

    classroom_id = fields.Many2one('school_management.classroom', string='Classroom', ondelete='cascade')
    exam_name = fields.Char(string='Exam Name')
    subject_1 = fields.Float(string='Subject 1')
    subject_2 = fields.Float(string='Subject 2')
    subject_3 = fields.Float(string='Subject 3')
    subject_4 = fields.Float(string='Subject 4')
