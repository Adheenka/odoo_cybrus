from odoo import fields, models, api
class SaleOrder(models.Model):
    _inherit = 'sale.order'


    related_estimation = fields.Many2one('sale', string='Appointment')

    estimation_line_ids = fields.One2many('estimation','estimation_i', string='Estimations')