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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_approved_user = fields.Boolean(string="Approver")
    approver_id = fields.Many2many('res.users',
                                   string="Approvers",
                                   default=lambda self: self.get_level_approvers())

    @api.model
    def get_level_approvers(self):
        approver_ids = []
        approval_model = self.env['purchase.approval'].sudo().search(
            [('approval_model_id', '=', 'purchase.order')], limit=1)
        print(approval_model, 'aaaa')
        if approval_model:
            for level in approval_model.level_ids:
                print('fff')
                if isinstance(level.user_ids, int):  # Check if user_ids is an ID
                    user_ids = [level.user_ids]
                else:
                    user_ids = level.user_ids.ids

                approver_ids += [(4, user_id) for user_id in user_ids]
        return approver_ids

    # def get_approve_user(self):
    #     print('heloo')
    #     for rec in self:
    #         print('heloo')
    #         rec.is_approved_user = True if self.env.user.id in rec.approver_id.ids else False
    #         print('ee')

    def button_submit_for_approval(self):
        # Add your logic here for submitting the purchase order for approval
        # You may want to create approval records, update statuses, etc.
        return True
