from odoo import fields, models, api ,_


# from odoo.addons.sale.models.sale_order import SaleOrder


class AccountMoveForm(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order ID",
                                  tracking=True)
    amount_untaxed = fields.Monetary(string='amount_untaxes',  store=True)
    gross_amount = fields.Monetary(string='Gross Amount',  store=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True,track_visibility='always')
    applied_discount = fields.Float(string='Applied Discount', digits='Discount', readonly=False)
    @api.onchange('sale_order_id')
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            sale_order = self.sale_order_id

            # Populate partner_id
            self.partner_id = sale_order.partner_id
            self.amount_total =sale_order.amount_total
            self.amount_untaxed =sale_order.amount_untaxed
            self.gross_amount = sale_order.gross_amount
            self.amount_tax = sale_order.amount_tax
            self.applied_discount = sale_order.applied_discount
            invoice_date = sale_order.date_order.strftime('%Y-%m-%d')

            # Assign the formatted date to invoice_date
            self.invoice_date = invoice_date

            # Clear existing invoice lines
            self.invoice_line_ids = [(5, 0, 0)]

            # Populate invoice lines from Sale Order lines
            for line in sale_order.order_line:
                invoice_line = self.env['account.move.line'].new({
                    'line_number':line.seq,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': line.product_uom_qty,

                    'price_unit': line.price_unit,

                    'tax_ids': [(6, 0, line.tax_id.ids)],
                    'price_subtotal': line.price_total,
                })




                self.invoice_line_ids += invoice_line
    #for expence code
    is_expense = fields.Boolean(string="Is Expense", default=False)