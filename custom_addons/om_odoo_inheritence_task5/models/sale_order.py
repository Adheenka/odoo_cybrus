from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    custom_user_id = fields.Many2one('res.users', string='Custom User')

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        for order in self:
            order.write({'custom_user_id': self.env.user.id})
        return res
