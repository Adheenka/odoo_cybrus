from odoo import fields, models, api ,_

class PurchaseApproval(models.Model):
    _name = 'purchase.approval'
    _description = 'Purchase Approval'

    approval_name = fields.Char(string='Approval Name')
    model = fields.Selection([
        ('purchase.order', 'Purchase Order'),
        # Add other models as needed
    ], string='Model')
    level_of_approval = fields.Integer(string='Level of Approval')

    approval_lines = fields.One2many(
        'purchase.approval.line',
        'approval_id',
        string='Approval Lines'
    )


class PurchaseApprovalLine(models.Model):
    _name = 'purchase.approval.line'
    _description = 'Purchase Approval Line'

    approval_id = fields.Many2one('purchase.approval', string='Approval')
    user_id = fields.Many2one('res.users', string='User', required=True)