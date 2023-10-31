from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError


# from odoo.addons.sale.models.sale_order import SaleOrder


class AccountMove(models.Model):
    _inherit = 'account.move'


    #for expence code
    is_expense = fields.Boolean(string="Is Expense")

    sequence = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)
    expense_line_ids = fields.One2many('account.move.line', 'move_id', string='Expense Lines')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('account.move.sequence') or 'New'

            # Get current date
            current_date = fields.Date.today()

            # Extract year and month from the current date
            year = fields.Date.from_string(current_date).year
            month = fields.Date.from_string(current_date).month

            # Format the sequence as required
            vals['sequence'] = f"EXP/{year}/{month:02d}/{sequence[-4:]}"

        return super(AccountMove, self).create(vals)

    # @api.model
    # def create(self, vals):
    #     if vals.get('sequence', 'New') == 'New':
    #         vals['sequence'] = self.env['ir.sequence'].next_by_code('account.move.sequence') or 'New'
    #     return super(AccountMove, self).create(vals)


    # @api.onchange('partner_id')
    # def onchange_partner(self):
    #     if self.is_expense:
    #         return {'domain': {'partner_id': [('is_expense_vendor', '=', True)]}}
    #     else:
    #         return super(AccountMoveForm, self).onchange_partner()
    # def _search_default_journal(self):
    #     if self.is_expense:
    #         if self.company_id.expense_journal_id:
    #             return self.company_id.expense_journal_id.id
    #         else:
    #             raise (ValidationError("No expense journal is configured"))
    #     else:
    #         return super(AccountMove, self)._search_default_journal()
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    price = fields.Float(string="Price")

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     if self.move_id.is_expense:
    #         return {'domain': {'product_id': [('is_expense', '=', True)]}}
    #     else:
    #         return super(AccountMoveLine, self)._onchange_product_id()

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     result = super(AccountMoveLine, self)._onchange_product_id()
    #
    #     if self.move_id.is_expense:
    #         domain = {'product_id': [('is_expense', '=', True)]}
    #         result['domain'] = result.get('domain', {}) | domain
    #     return result

class ProductError(models.Model):
    _inherit = 'product.template'

    expense_ok = fields.Boolean(string="product", default=False)