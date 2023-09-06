from odoo import fields, models



from odoo import models, fields

class CustomPosOrder(models.Model):
    _inherit = 'pos.order'

    # Add your custom fields here
    delivery_country = fields.Many2one('res.country', string='Delivery Country')
    delivery_type = fields.Selection([
        ('standard', 'Standard'),
        ('express', 'Express'),
    ], string='Delivery Type')
    expected_delivery_date = fields.Date('Expected Delivery Date')

