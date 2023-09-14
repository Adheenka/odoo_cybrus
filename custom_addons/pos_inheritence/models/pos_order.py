from odoo import models, fields, api

class CustomPosOrder(models.Model):
    _inherit = 'pos.order'

    # Add your custom fields here
    delivery_country = fields.Many2one('res.country', string='Delivery Country')
    delivery_type = fields.Selection([
        ('domestic', 'Domestic'),
        ('international', 'International'),
    ], string='Delivery Type')
    expected_delivery_date = fields.Date('Expected Delivery Date')
    card_number = fields.Char('Card Number')
    expiry_date = fields.Date('Expiry Date')

    @api.model
    def create_delivery_order(self, partner, delivery_country, delivery_type, expected_delivery_date):

        order = self.create({
            'partner_id': partner,
            'delivery_country': delivery_country,
            'delivery_type': delivery_type,
            'expected_delivery_date': expected_delivery_date,
        })
        return order
