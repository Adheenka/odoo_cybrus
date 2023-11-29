from odoo import models, fields, api


class PurchaseApproval(models.Model):
    _name = 'purchase.approval'
    _description = 'Purchase Approval'

    approval = fields.Char(string='Approval')
    approval_model_id = fields.Many2many('ir.model', string='Model')
    approval_levels = fields.Integer(string='Levels of Approval', default=1)
    need_approval = fields.Boolean(string='Need Approval', default=True)
    level_ids = fields.One2many('purchase.approval.level', 'approval_id', string='Approval Levels')

    @api.onchange('approval_levels')
    def _onchange_approval_levels(self):
        """Generate approval levels based on the 'Levels of Approval' field."""
        if self.approval_levels > 0:
            self.level_ids = [(5, 0, 0)]

            new_levels = []
            for level in range(1, self.approval_levels + 1):
                self.level_ids = [(0, 0, {
                    'level': f'Level {level}',
                })]
                self.level_ids = new_levels


class PurchaseApprovalLevel(models.Model):
    _name = 'purchase.approval.level'
    _description = 'Purchase Approval Level'

    approval_id = fields.Many2one('purchase.approval', string='Approval')
    level = fields.Char(string='Level', required=True)
    user_ids = fields.Many2many('res.users', string='Approvers')
    order_id = fields.Many2one('purchase.order', string="Purchase Order")


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_approver = fields.Boolean(string='Is Approver', compute='_compute_is_approver', store=True)
    approver_id = fields.Many2many('res.users',
                                   string="Approvers",
                                   default=lambda self: self.get_level_approvers())
    approval_status = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('approval', 'Approval'),
        ('approved', 'Approved'),
        ('purchase', 'Purchase Order'),
    ], string='Status', readonly=True, copy=False, tracking=True)

    # state = fields.Selection([
    #     ('draft', 'RFQ'),
    #     ('sent', 'RFQ Sent'),
    #     ('approved', 'Approved'),
    #     ('to approve', 'To Approve'),
    #     ('purchase', 'Purchase Order'),
    #     ('done', 'Locked'),
    #     ('cancel', 'Cancelled')
    # ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    @api.depends('approver_id')
    def _compute_is_approver(self):
        for record in self:
            record.is_approver = True if self.env.user.id in record.approver_id.ids else False

    @api.model
    def get_level_approvers(self):
        approver_ids = []
        approval_model = self.env['purchase.approval'].sudo().search(
            [('approval_model_id', '=', 'purchase.order')], limit=1)
        if approval_model:
            for level in approval_model.level_ids:
                if isinstance(level.user_ids, int):  # Check if user_ids is an ID
                    user_ids = [level.user_ids]
                else:
                    user_ids = level.user_ids.ids
                approver_ids += [(4, user_id) for user_id in user_ids]
        return approver_ids

    def button_submit_for_approval(self):
        approval_model = self.env['purchase.approval.level']

        for user in self.approver_id:
            # Check if the user has already approved
            existing_approval = approval_model.search([('order_id', '=', self.id), ('user_ids', 'in', user.ids)])
            if not existing_approval:
                # Create a new approval record for the user
                approval_model.create({
                    'order_id': self.id,
                    'user_ids': [(4, user.id)],
                    'level': f'Level {len(existing_approval) + 1}',
                })
                return True  # Return True after creating the approval for one user

        # Check if all approvers have approved
        approvals_count = approval_model.search_count([('order_id', '=', self.id)])
        if approvals_count == len(self.approver_id):
            self.write({'approval_status': 'approved'})

        return True