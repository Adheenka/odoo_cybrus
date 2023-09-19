from odoo import models, fields, api


class PosOrder(models.Model):
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
    def _default_delivery_country(self):
        partner = self.env.user.company_id.partner_id
        return partner.country_id

    def _get_delivery_details_popup(self):
        popup = self.env.ref('pos_inheritence.DeliveryDetailsPopup')
        return popup

    def action_show_delivery_details_popup(self):
        popup = self._get_delivery_details_popup()
        popup.show()

    def _action_apply_delivery_details(self, values):
        self.delivery_country = values['delivery_country_id']
        self.delivery_type = values['delivery_type']
        self.expected_delivery_date = values['expected_delivery_date']

    def _get_delivery_details(self):
        delivery_details = {
            'delivery_country_id': self.delivery_country.id,
            'delivery_type': self.delivery_type,
            'expected_delivery_date': self.expected_delivery_date,
        }
        return delivery_details
