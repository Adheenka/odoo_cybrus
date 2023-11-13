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


    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('account.move.sequence') or 'New'

            current_date = fields.Date.today()
            year = fields.Date.from_string(current_date).year
            month = fields.Date.from_string(current_date).month

            vals['sequence'] = f"EXP/{year}/{month:02d}/{sequence[-4:]}"

        return super(AccountMove, self).create(vals)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    price = fields.Float(string="Price")


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

    @api.depends('unit_price', 'quantity')
    def _get_subtotal(self):
        self.subtotal = self.unit_price * self.quantity


    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.unit_price = self.product_id.list_price