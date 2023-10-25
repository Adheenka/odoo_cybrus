from odoo import fields, models, api ,_


# from odoo.addons.sale.models.sale_order import SaleOrder


class AccountMoveForm(models.Model):
    _inherit = 'account.move'


    #for expence code
    is_expense = fields.Boolean(string="Is Expense", default=False)
    expense_sequence = fields.Char(string="Expense Sequence")
    @api.model
    def create(self, vals):
        if vals.get("move_type") == "in_invoice" and vals.get("is_expense"):
            vals["name"] = self.env["ir.sequence"].next_by_code('account.move.expense.sequence') or "New"
        return super(AccountMoveForm, self).create(vals)