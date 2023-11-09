from odoo import fields, models, api ,_
from odoo.exceptions import ValidationError
from odoo.tools import format_date


# from odoo.addons.sale.models.sale_order import SaleOrder


class AccountMove(models.Model):
    _inherit = 'account.move'


    #for expence code
    is_expense = fields.Boolean(string="Is Expense")

    sequence = fields.Char(string='Sequence', tracking=True, copy=False, readonly=True)
    expense_line_ids = fields.One2many('expense', 'account_move_id', string='Expense Lines')

    # def name_get(self):
    #     res = super(AccountMove, self).name_get()
    #     for rec in self:
    #         if rec.is_expense:
    #             new_name = f"EXP/{rec.date.year}/{rec.date.month:02d}/{rec.id:04d}"
    #         else:
    #             new_name = f"BILL/{rec.date.year}/{rec.date.month:02d}/{rec.id:04d}"
    #         res.append((rec.id, new_name))
    #     return res

    def name_get(self):
        result = super(AccountMove, self).name_get()
        for move in self:
            if self._context.get('name_groupby'):
                name = '**%s**, %s' % (format_date(self.env, move.date), move._get_move_display_name())
                if move.ref:
                    name += '     (%s)' % move.ref
                if move.partner_id.name:
                    name += ' - %s' % move.partner_id.name
            else:
                name = move._get_move_display_name(show_ref=True)

            if move.is_expense:  # Checking if move is an expense
                name = f"EXP/{format_date(self.env, move.date)}"  # Set name to EXP/YYYY/MM/XXXX

            result.append((move.id, name))
        return result
    # @api.depends('name', 'state')
    # def name_get(self):
    #     result = []
    #     for move in self:
    #         if self._context.get('name_groupby'):
    #             name = '**%s**, %s' % (format_date(self.env, move.date), move._get_move_display_name())
    #             if move.ref:
    #                 name += '     (%s)' % move.ref
    #             if move.partner_id.name:
    #                 name += ' - %s' % move.partner_id.name
    #         else:
    #             name = move._get_move_display_name(show_ref=True)
    #         result.append((move.id, name))
    #     return result

    # @api.depends('name', 'state')
    # def name_get(self):
    #     result = []
    #     for move in self:
    #         date_string = move.date.strftime('%Y/%m/%d')
    #         name = 'EXP/%s/%s' % (date_string, move.ref)
    #         result.append((move.id, name))
    #     return result

    @api.depends('sequence','is_expense')
        # def name_get(self):
        #     result = []
        #     for move in self:
        #         name = f"{move.sequence}"
        #         result.append((move.id, name))
        #     return result

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('account.move.sequence') or 'New'

            current_date = fields.Date.today()
            year = fields.Date.from_string(current_date).year
            month = fields.Date.from_string(current_date).month

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

class Expense(models.Model):
    _name = 'expense'
    _description = 'Expense'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    tax = fields.Float(string='Tax')
    account_move_id = fields.Many2one('account.move', string='Account Move')

    @api.depends('quantity', 'unit_price', 'tax')
    def _compute_total(self):
        for expense in self:
            expense.total = (expense.quantity * expense.unit_price) * (1 + expense.tax / 100)