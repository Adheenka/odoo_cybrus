from odoo import fields, models, api ,_


# from odoo.addons.sale.models.sale_order import SaleOrder


class AccountMove(models.Model):
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


            self.invoice_date = invoice_date


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

    #for email send code
    # def action_post(self):
    #
    #     super(AccountMove, self).action_post()
    #
    #
    #     for move in self:
    #         if move.move_type == 'out_invoice' and move.state == 'posted':
    #
    #             customer = move.partner_id
    #             customer_email = customer.email
    #
    #
    #             if customer_email:
    #                 mail_template = self.env.ref('sale_inheritence.email_template_post_invoice')
    #                 if mail_template:
    #
    #                     mail_template.write({
    #                         'email_to': customer_email
    #                     })
    #                     mail_template.send_mail(move.id, force_send=True)
    #
    #     return True

    def action_post(self):
        res = super(AccountMove, self).action_post()

        for move in self:
            if move.move_type == 'out_invoice' and move.state == 'posted':
                customer = move.partner_id
                customer_email = customer.email

                if customer_email:
                    mail_template = self.env.ref('sale_inheritence.email_template_post_invoice')
                    if mail_template:
                        mail_template.send_mail(move.id, force_send=True, email_values={'email_to': customer_email})
        return res
    # def action_post(self):
    #     # Invoke the original action_post method
    #     super(AccountMove, self).action_post()
    #
    #     # Add your custom logic to send email here
    #     # Example code to send an email after invoice confirmation
    #     for move in self:
    #         if move.move_type in ('out_invoice', 'in_invoice') and move.state == 'posted':
    #             # Check if it's an outgoing or incoming invoice and in 'posted' state
    #             mail_template = self.env.ref('account.email_template_edi_invoice')
    #             if mail_template:
    #                 # Replace with actual email sending logic, including recipients, email content, etc.
    #                 mail_template.send_mail(move.id, force_send=True)
    #     # End of example email sending logic
    #     return True

    # for msg send code
    # def action_post(self):
    #         result = super(AccountMove, self).action_post()
    #         for res in self:
    #             send_message_sms(res, res.partner_id, 'invoice_vaildate')
    #         return result


    #for expence code
    # is_expense = fields.Boolean(string="Is Expense", default=False)
    # expense_sequence = fields.Char(string="Expense Sequence")
    # @api.model
    # def create(self, vals):
    #     if vals.get("move_type") == "in_invoice" and vals.get("is_expense"):
    #         vals["name"] = self.env["ir.sequence"].next_by_code('account.move.expense.sequence') or "New"
    #     return super(AccountMoveForm, self).create(vals)