from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users',string="confirmed user")



    # def action_confirm(self):
    #     super(SaleOrder, self).action_confirm()
    #     self.confirmed_user_id = self.env.user.id

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        # print("invoice_vals",invoice_vals)
        invoice_vals['so_confirmed_user_id'] = self.confirmed_user_id.id
        return invoice_vals
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.write({'confirmed_user_id': self.env.user.id})
        return res

