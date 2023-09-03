from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    custom_user_id = fields.Many2one('res.users', string='Custom User')

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        for order in self:
            order.write({'custom_user_id': self.env.user.id})
        return res

    # def _prepare_invoice(self):
    #     invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
    #     # print("invoice_vals",invoice_vals)
    #     invoice_vals['so_confirmed_user_id'] = self.custom_user_id.name
    #     return invoice_vals
