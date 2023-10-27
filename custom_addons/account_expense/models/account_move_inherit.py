from odoo import fields, models, api ,_


# from odoo.addons.sale.models.sale_order import SaleOrder


class AccountMoveForm(models.Model):
    _inherit = 'account.move'


    #for expence code
    is_expense = fields.Boolean(string="Is Expense")
    expense_sequence = fields.Char(string="Expense Sequence")
    expense_line_ids = fields.One2many('account.move.line', 'move_id', string='Expense Lines')
    @api.model
    def create(self, vals):
        if vals.get("move_type") == "in_invoice" and vals.get("is_expense"):
            vals["name"] = self.env["ir.sequence"].next_by_code('account.move.expense.sequence') or "New"
        return super(AccountMoveForm, self).create(vals)

    # @api.onchange('partner_id')
    # def onchange_partner(self):
    #     if self.is_expense:
    #         return {'domain': {'partner_id': [('is_expense_vendor', '=', True)]}}
    #     else:
    #         return super(AccountMoveForm, self).onchange_partner()
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    price = fields.Float(string="Price")